#!/usr/bin/env python3
"""TASKS/00_TASK_LIST.md 감사.

사용: python scripts/audit_tasks.py [--root .] [--tasks-dir TASKS] [--list 00_TASK_LIST.md]
종료 코드: 0 = 통과, 1 = 오류 있음

00_TASK_LIST.md 형식
  ## 2. Task List       16열 표 (아래 COLUMNS)
  ## 4. Requirement 추적표   | Requirement | Status | 구현 Task | Test / Manual Check Task |
  ## 5. NON_IMPLEMENTATION   | Requirement | 제외 근거 | 후속 방향 |
상세 파일 TASKS/TASK-<Task ID>.md 는 구현 Task마다 하나씩 있어야 하며(1:1), 14개 절과 목록 값(Requirement Ref·
Depends On·Expected Files·Page Entry·AC 항목 수)이 Task List 행과 일치해야 한다. scripts/gen_task_details.py 가 생성한다.
"""
import argparse
import json
import re
import sys
from pathlib import Path

COLUMNS = ["Seq", "Task ID", "제목", "Category", "Implementation Status", "Requirement Ref",
           "Screen", "Route", "Page Entry", "Depends On", "Expected Files",
           "Functional AC", "Visual AC", "Security/Privacy AC", "Verify", "Priority"]
CATEGORIES = {"FOUNDATION", "DATA", "LOGIC", "DB", "API", "COMPONENT", "PAGE", "TEST", "E2E", "MANUAL", "OPS"}
VERIFY_CATS = {"TEST", "E2E", "MANUAL"}
CODE_CATS = {"PAGE", "COMPONENT", "API"}
PRIORITIES = {"P0", "P1", "P2"}
ALLOWED_TABLES = {"diagnosis_inputs", "diagnosis_results", "deduction_items", "recommendation_items"}
MAX_TABLES = 4
MAX_E2E = 3
TASK_ID_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$")
REQ_RE = re.compile(r"REQ-(?:FUNC|NFR)-[A-Z]+(?:-\d{3})?")
ROW_RE = re.compile(r"^\|\s*(REQ-(?:FUNC|NFR)-[A-Z]+(?:-\d{3})?)\s*\|(.*)\|\s*$")
FILE_VERBS = {"create", "modify", "delete"}

FORBIDDEN = [
    (re.compile(r"\bEC2\b|\bAWS\b|\bS3 bucket\b", re.I), "AWS·EC2 관련 Task 금지"),
    (re.compile(r"auto[- ]?merge|자동\s*merge|자동\s*머지", re.I), "자동 Merge Task 금지"),
    (re.compile(r"\bfirefox\b|\bwebkit\b", re.I), "Playwright는 Chromium만 허용"),
    (re.compile(r"항공|숙소|동행|여행지|travel-tools|/mates|/account|Guest|Member", re.I), "Traveler 잔재 용어"),
    (re.compile(r"로그인|회원가입|관리자 화면|결제|구독|별점|광고 배너", re.I), "v1 범위 밖 기능 용어"),
    (re.compile(r"Lorem ipsum|준비 중|정보 확인 필요", re.I), "Placeholder 문구"),
]
# 같은 문장에서 '금지/제외/않' 등으로 부정된 용어는 허용
NEGATION_RE = re.compile(r"금지|제외|없|않|만들지|EXCLUDED|아니|대체")

PAGE_OWNER_SECTIONS = {
    "SCR-001": ["Hero", "필수 정보", "선택 정보", "3단계", "CTA"],
    "SCR-002": ["Hero", "게이지", "근거", "Chip", "Drawer", "CTA", "재진단"],
    "SCR-003": ["Intro", "Card Grid", "Empty State", "3단계", "CTA"],
    "SCR-004": ["Intro", "Card Grid", "Empty State", "CTA"],
    "SCR-005": ["Intro", "16유형", "강점", "유의점", "CTA"],
}
PAGE_OWNER_MIN_COUNT = {
    "SCR-001": ["필수 필드 3", "선택 필드 2"],
    "SCR-002": ["카테고리 4"],
    "SCR-003": ["6개"],
    "SCR-004": ["6개"],
    "SCR-005": ["16개"],
}
PAGE_OWNER_COMMON = ["Section 순서", "Section별 데이터 출처", "Empty State", "Lorem ipsum", "빈 영역", "Preview"]


class Audit:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, m):
        self.errors.append(m)

    def warn(self, m):
        self.warnings.append(m)


def split_cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_sep(line):
    return set(line.replace("|", "").strip()) <= set("-: ")


def ticks(cell):
    """셀에서 백틱으로 감싼 값 목록. '—'이면 빈 목록."""
    return re.findall(r"`([^`]+)`", cell)


def segments(cell):
    return [s.strip() for s in re.split(r"<br>", cell) if s.strip()]


def parse_doc(text, au):
    """섹션별 표를 {섹션 키: [셀 목록]}으로 읽는다."""
    tables, section = {"tasks": [], "trace": [], "nonimpl": []}, None
    summary = text.split("## 1.")[0]
    for line in text.splitlines():
        if line.startswith("## "):
            h = line[3:].strip()
            section = ("tasks" if "Task List" in h else "trace" if "추적표" in h
                       else "nonimpl" if "NON_IMPLEMENTATION" in h else None)
            continue
        if section is None or not line.startswith("|") or is_sep(line):
            continue
        cells = split_cells(line)
        if cells[0] in ("Seq", "Requirement"):
            if section == "tasks" and cells != COLUMNS:
                au.err(f"Task List 열이 규격과 다름: {cells}")
            continue
        tables[section].append(cells)
    return tables, summary


def parse_task(cells, au):
    if len(cells) != len(COLUMNS):
        au.err(f"Task 행 열 수 {len(cells)} != {len(COLUMNS)}: {cells[:2]}")
        return None
    r = dict(zip(COLUMNS, cells))
    tid = (ticks(r["Task ID"]) or [r["Task ID"]])[0]
    files = []
    for f in ticks(r["Expected Files"]):
        verb, _, path = f.partition(" ")
        files.append((verb, path.strip()))
    return {
        "seq": r["Seq"], "id": tid, "title": r["제목"], "cat": r["Category"], "status": r["Implementation Status"],
        "reqs": ticks(r["Requirement Ref"]), "screen": r["Screen"], "route": (ticks(r["Route"]) or ["—"])[0],
        "entry": (ticks(r["Page Entry"]) or ["—"])[0], "deps": ticks(r["Depends On"]), "files": files,
        "fac": r["Functional AC"], "vac": r["Visual AC"], "sac": r["Security/Privacy AC"],
        "verify": r["Verify"], "pri": r["Priority"],
        "blob": " ".join(cells),
    }


def find_cycle(graph):
    state = {}

    def visit(n, path):
        state[n] = 1
        for m in graph.get(n, []):
            if m not in graph:
                continue
            if state.get(m) == 1:
                return path + [n, m]
            if state.get(m) is None:
                r = visit(m, path + [n])
                if r:
                    return r
        state[n] = 2
        return None

    for n in graph:
        if state.get(n) is None:
            r = visit(n, [])
            if r:
                return r
    return None


DETAIL_SECTIONS = ["Context", "Project Scope", "Requirement Ref", "Screen / Route / Page Entry", "Design Ref",
                   "Depends On", "Expected Files", "Functional AC", "Visual AC", "Security/Privacy AC",
                   "Test Cases", "Verify", "Definition of Done", "Forbidden"]


def detail_sections(text):
    out, cur = {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            cur = line[3:].strip()
            out[cur] = []
        elif cur is not None:
            out[cur].append(line)
    return out


def check_detail(t, text, au):
    """TASKS/TASK-<ID>.md 가 Task List 행과 일치하는지 검사한다."""
    tid = t["id"]
    sec = detail_sections(text)
    if f"- Task ID: {tid}" not in text:
        au.err(f"{tid}: 상세 파일의 Task ID 불일치")
    missing = [s for s in DETAIL_SECTIONS if s not in sec]
    if missing:
        au.err(f"{tid}: 상세 파일에 절 누락 {missing}")
        return
    if list(sec) != DETAIL_SECTIONS:
        au.err(f"{tid}: 상세 파일 절 순서·구성이 규격과 다름")
    body = {k: "\n".join(v) for k, v in sec.items()}
    reqs = sorted(re.findall(r"^- (REQ-[A-Z]+-[A-Z]+(?:-\d{3})?)", body["Requirement Ref"], re.M))
    if reqs != sorted(t["reqs"]):
        au.err(f"{tid}: Requirement Ref 불일치(목록 {sorted(t['reqs'])} / 상세 {reqs})")
    deps = sorted(re.findall(r"^- `([^`]+)`", body["Depends On"], re.M))
    if deps != sorted(t["deps"]):
        au.err(f"{tid}: Depends On 불일치(목록 {sorted(t['deps'])} / 상세 {deps})")
    files = sorted(re.findall(r"^- (create|modify|delete): (\S+)", body["Expected Files"], re.M))
    if files != sorted(t["files"]):
        au.err(f"{tid}: Expected Files 불일치")
    if "Expected Files 밖 수정 금지" not in body["Expected Files"]:
        au.err(f"{tid}: Expected Files 밖 수정 금지 문구 없음")
    entry = (re.search(r"^- Page Entry: (.+)$", body["Screen / Route / Page Entry"], re.M) or [None, ""])[1].strip("` ")
    if (entry or "—") != t["entry"]:
        au.err(f"{tid}: Page Entry 불일치(목록 {t['entry']} / 상세 {entry})")
    for name, col in (("Functional AC", "fac"), ("Visual AC", "vac"), ("Security/Privacy AC", "sac")):
        n_detail = len(re.findall(r"^\d+\. ", body[name], re.M))
        if n_detail != len(segments(t[col])):
            au.err(f"{tid}: {name} 항목 수 불일치(목록 {len(segments(t[col]))} / 상세 {n_detail})")
    if "- [ ]" not in body["Definition of Done"]:
        au.err(f"{tid}: Definition of Done 체크 항목 없음")
    if re.search(r"6개 테이블|테이블 6개", text):
        au.err(f"{tid}: DB 테이블 수는 4개다(6개 표기 금지)")
    if t["cat"] == "PAGE" and "하위 Component" not in text:
        au.err(f"{tid}: Page Owner 상세에 'Page 조립만' 범위 문구 없음")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--tasks-dir", default="TASKS")
    ap.add_argument("--list", default="00_TASK_LIST.md")
    a = ap.parse_args()
    root = Path(a.root).resolve()
    tdir = root / a.tasks_dir
    au = Audit()

    contract_p = root / "design-reference/SCREEN_ROUTE_CONTRACT.json"
    scope_p = root / "docs/PROJECT_SCOPE.md"
    list_p = tdir / a.list
    for p in (contract_p, scope_p, list_p):
        if not p.is_file():
            au.err(f"파일 없음: {p.relative_to(root)}")
    if au.errors:
        return report(au, 0)

    contract = json.loads(contract_p.read_text(encoding="utf-8"))
    screens = {s["screen_id"]: s for s in contract["screens"]}
    scope = {}
    for line in scope_p.read_text(encoding="utf-8").splitlines():
        m = ROW_RE.match(line)
        if m:
            cells = split_cells("|" + m.group(2) + "|")
            if cells[0] in ("IMPLEMENT", "EXCLUDED"):
                scope[m.group(1)] = cells[0]

    tables, summary = parse_doc(list_p.read_text(encoding="utf-8"), au)
    tasks = [t for t in (parse_task(c, au) for c in tables["tasks"]) if t]
    ids = [t["id"] for t in tasks]
    by_id = {t["id"]: t for t in tasks}

    # ---- 1. ID·Category·Status·요약 -----------------------------------------
    if len(set(ids)) != len(ids):
        au.err("Task List에 중복 Task ID")
    for i, t in enumerate(tasks, 1):
        if t["seq"] != str(i):
            au.err(f"{t['id']}: Seq {t['seq']} (기대 {i})")
        if not TASK_ID_RE.match(t["id"]):
            au.err(f"{t['id']}: Task ID 형식 오류(대문자-하이픈)")
        if t["cat"] not in CATEGORIES:
            au.err(f"{t['id']}: 알 수 없는 Category '{t['cat']}' (허용: {sorted(CATEGORIES)})")
        if t["status"] != "IMPLEMENT":
            au.err(f"{t['id']}: Implementation Status가 IMPLEMENT가 아님({t['status']}) — EXCLUDED는 Task로 만들지 않는다")
        if t["pri"] not in PRIORITIES:
            au.err(f"{t['id']}: Priority '{t['pri']}' (허용: {sorted(PRIORITIES)})")
        for col in ("fac", "vac", "sac", "verify"):
            if not t[col] or t[col] in ("—", "-"):
                au.err(f"{t['id']}: {col} 비어 있음")
        if not t["files"]:
            au.err(f"{t['id']}: Expected Files 없음")
    m = re.search(r"Task 총 \*\*(\d+)개\*\*", summary)
    if not m or int(m.group(1)) != len(tasks):
        au.err(f"요약의 Task 수({m.group(1) if m else '없음'})가 표의 행 수({len(tasks)})와 다름")
    cat_line = re.search(r"Category별:(.*)", summary)
    if cat_line:
        stated = {k: int(v) for k, v in re.findall(r"([A-Z0-9]+) (\d+)", cat_line.group(1))}
        actual = {}
        for t in tasks:
            actual[t["cat"]] = actual.get(t["cat"], 0) + 1
        if stated != actual:
            au.err(f"요약의 Category별 수 {stated} != 실제 {actual}")
    else:
        au.err("요약에 Category별 수가 없음")

    # 상세 파일 TASKS/TASK-<ID>.md 와 구현 Task ID의 1:1 대조
    detail_files = {p.name[len("TASK-"):-len(".md")]: p for p in tdir.glob("TASK-*.md")}
    impl_ids = [t["id"] for t in tasks if t["status"] == "IMPLEMENT"]
    for tid in impl_ids:
        if tid not in detail_files:
            au.err(f"{tid}: 상세 파일 TASKS/TASK-{tid}.md 없음")
    for did in detail_files:
        if did not in impl_ids:
            au.err(f"TASK-{did}.md: Task List의 구현 Task가 아님(고아 파일 또는 EXCLUDED)")
    for t in tasks:
        p = detail_files.get(t["id"])
        if p:
            check_detail(t, p.read_text(encoding="utf-8"), au)

    # ---- 2. 의존성 -----------------------------------------------------------
    graph = {t["id"]: t["deps"] for t in tasks}
    for t in tasks:
        for dep in t["deps"]:
            if dep not in graph:
                au.err(f"{t['id']}: 존재하지 않는 의존 Task {dep}")
            if dep == t["id"]:
                au.err(f"{t['id']}: 자기 자신에 의존")
    cyc = find_cycle(graph)
    if cyc:
        au.err("의존성 순환: " + " -> ".join(cyc))

    # ---- 3. Page Owner -------------------------------------------------------
    owners = {}
    for t in tasks:
        if t["cat"] == "PAGE":
            owners.setdefault(t["screen"], []).append(t)
    for sid in screens:
        n = len(owners.get(sid, []))
        if n != 1:
            au.err(f"{sid}: Page Owner Task가 {n}개(정확히 1개 필요)")
    for sid in owners:
        if sid not in screens:
            au.err(f"계약에 없는 Screen의 Page Owner: {sid}")
    page_entries = {s["page_entry"]: sid for sid, s in screens.items()}
    for sid, lst in owners.items():
        if sid not in screens or len(lst) != 1:
            continue
        t = lst[0]
        s = screens[sid]
        if t["entry"] != s["page_entry"]:
            au.err(f"{t['id']}: Page Entry {t['entry']} != 계약 {s['page_entry']}")
        if t["route"] != s["route"]:
            au.err(f"{t['id']}: Route {t['route']} != 계약 {s['route']}")
        if not any(f == s["page_entry"] and v in ("create", "modify") for v, f in t["files"]):
            au.err(f"{t['id']}: Page Owner Expected Files에 {s['page_entry']} 없음")
        extra = [f for v, f in t["files"] if f != s["page_entry"]]
        if extra:
            au.err(f"{t['id']}: Page Owner는 Route Page 조립만 범위 — Expected Files에 {extra} 포함")
        need = [c["id"] for c in tasks
                if c["cat"] in ("COMPONENT", "API", "DATA") and sid in [x.strip() for x in c["screen"].split(",")]]
        for c in need:
            if c not in t["deps"]:
                au.err(f"{t['id']}: 같은 Screen의 Component·API·Data Task {c}에 의존하지 않음")
        if not any(by_id[c]["cat"] == "COMPONENT" for c in need):
            au.err(f"{sid}: Component Task가 하나도 없음(Page Owner와 구분 필요)")
        for dep in t["deps"]:
            if dep in by_id and by_id[dep]["cat"] == "PAGE":
                au.err(f"{t['id']}: 다른 Page Owner({dep})에 의존 — 공유 코드는 Component/Foundation Task로 분리")
        ac = " ".join([t["fac"], t["vac"], t["verify"]])
        for kw in PAGE_OWNER_COMMON + PAGE_OWNER_SECTIONS[sid] + PAGE_OWNER_MIN_COUNT[sid]:
            if kw not in ac:
                au.err(f"{t['id']}({sid}): Page Owner AC에 '{kw}' 누락")
        if sid == "SCR-001" and "Starter" not in ac:
            au.err(f"{t['id']}: SCR-001 Owner AC에 Starter 템플릿 금지 없음")
    # 한 Task가 여러 Page Entry를, 여러 Task가 같은 Page Entry를 소유하지 않는다
    entry_owner = {}
    for t in tasks:
        if t["entry"] == "—":
            continue
        if t["entry"] in entry_owner:
            au.err(f"{t['id']}: Page Entry {t['entry']}를 {entry_owner[t['entry']]}도 소유함")
        entry_owner[t["entry"]] = t["id"]
        owned = [f for v, f in t["files"] if f in page_entries or f == "src/app/page.tsx"]
        if len(set(owned)) > 1:
            au.err(f"{t['id']}: 여러 Page Entry를 동시에 다룸 {sorted(set(owned))}")
    for t in tasks:
        if t["cat"] == "PAGE":
            continue
        for v, f in t["files"]:
            if f in page_entries and v == "create":
                au.err(f"{t['id']}: Page Owner가 아닌 Task가 Page Entry {f}를 생성함")

    # ---- 4. src/app/page.tsx Owner(Starter 제거) ---------------------------
    root_owners = [t for t in tasks if any(f == "src/app/page.tsx" for _, f in t["files"])]
    if not root_owners:
        au.err("src/app/page.tsx를 다루는 Task가 없음(Starter 제거 필요)")
    if len(root_owners) > 1:
        au.err("src/app/page.tsx를 여러 Task가 소유: " + ", ".join(t["id"] for t in root_owners))
    for t in root_owners:
        ac = t["fac"] + t["vac"]
        if "Starter" not in ac or "redirect" not in ac:
            au.err(f"{t['id']}: src/app/page.tsx Owner AC에 Starter 제거·/diagnosis redirect 없음")

    # ---- 5. Expected Files 실제 파일 트리 ----------------------------------
    owner_of = {}
    for t in tasks:
        for verb, f in t["files"]:
            if verb not in FILE_VERBS:
                au.err(f"{t['id']}: Expected Files 동사 오류 '{verb}' ({f})")
                continue
            if f.startswith("/") or ".." in Path(f).parts:
                au.err(f"{t['id']}: 상대 경로가 아님 {f}")
                continue
            exists = (root / f).exists()
            if verb in ("modify", "delete") and not exists:
                au.err(f"{t['id']}: {verb} 대상이 존재하지 않음 {f}")
            if verb == "create" and exists:
                au.err(f"{t['id']}: create 대상이 이미 존재함 {f} (modify로 바꾸거나 제거)")
            if verb == "create":
                if f in owner_of:
                    au.err(f"{t['id']}: {owner_of[f]}와 같은 파일을 create함 {f}")
                owner_of[f] = t["id"]

    # ---- 6. Requirement 커버리지 -------------------------------------------
    trace = {}
    for c in tables["trace"]:
        if len(c) < 4:
            au.err(f"추적표 행 형식 오류: {c}")
            continue
        trace[c[0]] = {"status": c[1], "impl": ticks(c[2]), "test": ticks(c[3])}
    nonimpl = {c[0] for c in tables["nonimpl"]}
    referenced = {}
    for t in tasks:
        for r in t["reqs"]:
            if not REQ_RE.fullmatch(r):
                au.err(f"{t['id']}: Requirement 형식 오류 {r}")
                continue
            referenced.setdefault(r, []).append(t)
    for rid, st in scope.items():
        c = trace.get(rid)
        if not c:
            au.err(f"{rid}: Requirement 추적표에 없음")
            continue
        if c["status"] != st:
            au.err(f"{rid}: PROJECT_SCOPE({st})와 추적표({c['status']}) 불일치")
        got = referenced.get(rid, [])
        if st == "IMPLEMENT":
            impl = {t["id"] for t in got if t["cat"] not in VERIFY_CATS}
            test = {t["id"] for t in got if t["cat"] in VERIFY_CATS}
            if not impl:
                au.err(f"{rid}: IMPLEMENT인데 구현 Task가 없음")
            if not test:
                au.err(f"{rid}: IMPLEMENT인데 Test/Manual Check Task가 없음")
            if set(c["impl"]) != impl:
                au.err(f"{rid}: 추적표 구현 Task {sorted(c['impl'])} != Task List 참조 {sorted(impl)}")
            if set(c["test"]) != test:
                au.err(f"{rid}: 추적표 Test Task {sorted(c['test'])} != Task List 참조 {sorted(test)}")
            if rid in nonimpl:
                au.err(f"{rid}: IMPLEMENT인데 NON_IMPLEMENTATION에 있음")
        else:
            if got:
                au.err(f"{rid}: EXCLUDED인데 Task가 연결됨 {sorted(t['id'] for t in got)}")
            if rid not in nonimpl:
                au.err(f"{rid}: EXCLUDED인데 NON_IMPLEMENTATION 표에 근거가 없음")
    for rid in list(trace) + list(nonimpl):
        if rid not in scope:
            au.err(f"{rid}: PROJECT_SCOPE에 없는 Requirement")

    # ---- 7. DB 테이블 -------------------------------------------------------
    db_text = " ".join(t["blob"] for t in tasks if t["cat"] == "DB")
    found = {n for n in ALLOWED_TABLES if n in db_text}
    for n in sorted(ALLOWED_TABLES - found):
        au.err(f"DB Task에 테이블 {n} 정의가 없음")
    for n in re.findall(r"테이블 (\d+)개", db_text):
        if int(n) != MAX_TABLES:
            au.err(f"DB 테이블 수 표기 {n}개 != {MAX_TABLES}")
    for bad in re.findall(r"`?(users?|accounts?|payments?|admins?|sessions?|profiles?)`?\s*테이블", db_text):
        au.err(f"허용되지 않은 테이블 '{bad}'")
    for t in tasks:
        if t["cat"] == "DB" and "desired_job" in t["blob"]:
            au.err(f"{t['id']}: 희망 직무 DB 컬럼(desired_job)은 결정 D-02 전까지 추가 금지")

    # ---- 8. Playwright / 금지 용어 / Next.js 문서 --------------------------
    e2e = [t for t in tasks if t["cat"] == "E2E"]
    if not 2 <= len(e2e) <= MAX_E2E:
        au.err(f"E2E(Playwright) Task {len(e2e)}개 (2~{MAX_E2E}개로 묶어야 함)")
    for t in tasks:
        blob = t["blob"]
        if re.search(r"playwright", blob, re.I) and t["cat"] not in ("E2E", "FOUNDATION", "OPS", "MANUAL"):
            au.err(f"{t['id']}: Playwright는 E2E·설정 Task에서만 사용")
        if t["cat"] == "E2E" and "chromium" not in blob.lower():
            au.err(f"{t['id']}: E2E Task에 Chromium 명시 없음")
        for rx, msg in FORBIDDEN:
            for col in ("title", "fac", "vac", "sac", "verify"):
                for seg in segments(t[col]):
                    if rx.search(seg) and not NEGATION_RE.search(seg):
                        au.err(f"{t['id']}: {msg} — '{seg[:60]}'")
        if t["cat"] in CODE_CATS and "node_modules/next/dist/docs" not in blob:
            au.err(f"{t['id']}: Next.js 문서(node_modules/next/dist/docs) 확인 AC 없음")
        elif t["cat"] in ("FOUNDATION", "DB") and "node_modules/next/dist/docs" not in blob and t["cat"] == "FOUNDATION":
            au.warn(f"{t['id']}: Next.js 문서 확인 AC 없음")
    return report(au, len(tasks))


def report(au, n):
    print(f"Task {n}개 감사 (개수는 완료 조건이 아님)")
    for w in au.warnings:
        print(f"WARN  {w}")
    for e in au.errors:
        print(f"ERROR {e}")
    ok = not au.errors
    print("RESULT:", "PASS" if ok else f"FAIL ({len(au.errors)} errors)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
