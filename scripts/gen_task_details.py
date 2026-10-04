#!/usr/bin/env python3
"""TASKS/00_TASK_LIST.md의 구현 Task를 TASKS/TASK-<ID>.md 상세 파일로 변환한다.

사용: python scripts/gen_task_details.py [--root .] [--only ID ...]
- Task List가 정본이다. 같은 ID 파일은 덮어써 갱신하며 중복 파일을 만들지 않는다.
- Implementation Status가 IMPLEMENT가 아닌 행(EXCLUDED)은 파일을 만들지 않는다.
- 구현 코드·Branch·Commit을 만들지 않는다.
종료 코드: 0 = 생성, 1 = 입력 검사 실패
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_tasks import (Audit, CATEGORIES, COLUMNS, PRIORITIES, ROW_RE, VERIFY_CATS,  # noqa: E402
                         parse_doc, parse_task, split_cells, segments, find_cycle)

SECTIONS = ["Context", "Project Scope", "Requirement Ref", "Screen / Route / Page Entry", "Design Ref",
            "Depends On", "Expected Files", "Functional AC", "Visual AC", "Security/Privacy AC",
            "Test Cases", "Verify", "Definition of Done", "Forbidden"]

SRS_SECTION = {"DIAG": "§4.3.1", "SCORE": "§4.3.2", "RECO": "§4.3.3", "JOBLINK": "§4.3.3b",
               "ATTITUDE": "§4.3.3c", "PERF": "§4.4.1", "AVAIL": "§4.4.2", "SEC": "§4.4.3",
               "PRIV": "§4.4.3", "OBS": "§4.4.4"}

D = "design-reference/D-001/DESIGN.md"
U = "design-reference/UI_CONTRACT.md"
C = "design-reference/SCREEN_ROUTE_CONTRACT.json"
NONE_DESIGN = "해당 없음 — 시각 규칙이 없는 Task다. 화면에 영향이 생기면 D-001 Token만 사용한다."
DESIGN_BY_ID = {
    "FND-TEST-TOOLING": [NONE_DESIGN],
    "FND-TOKENS": [f"`{D}` §1 Visual Theme, §2 Color Token, §3 Typography, §4 Spacing, §5 Radius, §6 Shadow, §16 Page Section 최대 폭, §21 Do / Do Not"],
    "FND-ROOT-REDIRECT": [f"`{U}` §0 공통 계약(`/`는 Screen이 아닌 기술 Route)", f"`{C}` technical_routes(`/`)"],
    "FND-NOT-FOUND": [f"`{D}` §14 Loading · Empty · Error, §20 완성형 Empty State · Placeholder 금지", f"`{C}` technical_routes(`*`)"],
    "FND-SHELL": [f"`{D}` §7 Header · Footer, §15 Desktop · Mobile 규칙", f"`{U}` §0 공통 계약(Header 탭 5개·Breadcrumb)", f"`{C}` required_navigation(HEADER)"],
    "FND-FEEDBACK": [f"`{D}` §13 Alert · Toast, §14 Loading · Empty · Error, §20 Placeholder 금지"],
    "FND-SECTIONS": [f"`{D}` §16 Page Section 최대 폭, §17 Hero 높이, §18 Section별 위계와 시각적 리듬"],
    "FND-SESSION-GUARD": [f"`{D}` §13 Alert(warning), §14 Error(진단 미완료 접근)", f"`{U}` SCR-002~004 상태"],
    "DATA-RECOMMENDATIONS": [f"`{D}` §9 Recommendation Card, §20 Placeholder 금지", f"`{U}` SCR-003"],
    "DATA-JOBSITES": [f"`{D}` §21 Do Not(사이트 로고 이미지 금지)", f"`{U}` SCR-004"],
    "DATA-MBTI-ATTITUDE": [f"`{U}` SCR-005", f"`{D}` §21 Do(참고용 고지)"],
    "CMP-FIELDS": [f"`{D}` §10 Form · Tabs, §15 Desktop · Mobile 규칙, §20 placeholder 예시 값 규칙", f"`{U}` SCR-001 주요 Component"],
    "CMP-DIAG-FORM": [f"`{D}` §10 Form · Tabs, §14 Error, §15 Desktop · Mobile 규칙", f"`{U}` SCR-001 상태·금지 기능"],
    "CMP-SCORE-HERO": [f"`{D}` §3 type.score, §15, §17 Hero 높이", f"`{U}` SCR-002 주요 Component"],
    "CMP-REASON-DRAWER": [f"`{D}` §12 Drawer · Modal, §14 Loading · Error, §15", f"`{U}` SCR-002 상태·이동"],
    "CMP-DEDUCTION-CHIPS": [f"`{D}` §11 Result Item Card, §18 Section별 위계", f"`{U}` SCR-002 영역 순서 4"],
    "CMP-RECO-GRID": [f"`{D}` §9 Recommendation Card, §14 Empty(SCR-003), §15 Card Grid", f"`{U}` SCR-003"],
    "CMP-JOB-SITES": [f"`{D}` §8 Search · Filter, §9 Card, §14 Empty(SCR-004), §21 Do", f"`{U}` SCR-004"],
    "CMP-MBTI-GRID": [f"`{D}` §15 Desktop · Mobile 규칙(4×4 / 2열), §19 SCR-005", f"`{U}` SCR-005"],
    "CMP-ATTITUDE-PANEL": [f"`{D}` §14 Empty(SCR-005), §18, §21 Do·Do Not", f"`{U}` SCR-005 금지 기능·고지"],
    "MANUAL-PREVIEW": [f"`{D}` §15~§20, §22 검증 체크", f"`{U}` 5개 Screen 전체"],
    "RELEASE-CHECK": [f"`{D}` §21 Do / Do Not, §22 검증 체크", f"`{U}` §0 공통 금지"],
}
PAGE_D = f"`{D}` §16 Page Section 최대 폭, §17 Hero 높이, §18 Section별 위계, §19 화면별 Section 순서와 최소 콘텐츠 수, §20 완성형 Empty State · Placeholder 금지"

ROLE = {
    "FOUNDATION": "여러 Screen이 공유하는 기반을 만든다.",
    "DATA": "`src/data`의 하드코딩 정적 데이터를 만든다(외부 연동·DB 저장 없음).",
    "LOGIC": "UI와 무관한 순수 함수를 만들어 단위 테스트로 검증 가능하게 한다.",
    "DB": "관리형 DB의 4개 테이블 범위 안에서 스키마·접근 제어·접근 함수를 만든다.",
    "API": "서버 Route Handler(또는 이벤트 기록)를 만든다.",
    "COMPONENT": "화면에 쓰이는 컴포넌트를 만든다. Page Entry는 만들지 않는다.",
    "PAGE": "Route Page(Page Entry)를 조립한다. 하위 Component를 새로 만들지 않고 import·상태 전환·데이터 연결만 한다.",
    "TEST": "구현이 Requirement와 AC를 만족하는지 자동 테스트로 확인한다.",
    "E2E": "Playwright(Chromium)로 핵심 흐름을 확인한다.",
    "MANUAL": "자동화하지 않는 항목을 수동으로 확인하고 증거를 남긴다.",
    "OPS": "CI 또는 배포·DB 연결 점검을 수행한다.",
}
DOD_COMMON = [
    "Functional AC·Visual AC·Security/Privacy AC 항목을 모두 충족했다",
    "Verify의 명령·확인을 실행해 결과를 기록했다(통과하지 못하면 완료로 보고하지 않는다)",
    "Expected Files에 없는 파일을 수정하지 않았다",
    "Forbidden 항목에 해당하는 변경이 없다",
]
DOD_BY_CAT = {
    "PAGE": ["Desktop(1440)·Mobile(390) Preview에서 Section 순서·최소 콘텐츠 수·Empty State를 확인했다", "구현 전 `node_modules/next/dist/docs/` 관련 문서를 확인했다"],
    "COMPONENT": ["구현 전 `node_modules/next/dist/docs/` 관련 문서를 확인했다", "`npm run lint`·`npm run build`가 통과한다"],
    "API": ["구현 전 `node_modules/next/dist/docs/` 관련 문서를 확인했다", "`npm run lint`·`npm run build`가 통과한다"],
    "FOUNDATION": ["`npm run lint`·`npm run build`가 통과한다"],
    "LOGIC": ["대응 단위 테스트가 통과한다"],
    "DATA": ["대응 단위 테스트가 통과하고 빈 필드가 없다"],
    "DB": ["테이블이 4개를 넘지 않는다(`diagnosis_inputs`, `diagnosis_results`, `deduction_items`, `recommendation_items`)"],
    "TEST": ["테스트가 현재 구현에서 통과한다"],
    "E2E": ["Chromium project에서만 실행해 통과한다"],
    "MANUAL": ["`TASKS/evidence/`에 확인 결과를 기록했다"],
    "OPS": ["실행 결과를 기록했다"],
}
FORBID_COMMON = [
    "Expected Files 밖 파일 수정·생성 금지(필요하면 먼저 `TASKS/00_TASK_LIST.md`를 고친다)",
    "로그인·계정·관리자·결제·별점·광고 UI·Route 추가 금지",
    "D-001 Token에 없는 색·간격·그림자 추가 금지",
    "`Lorem ipsum`·`준비 중`·`정보 확인 필요`·`TBD` 등 Placeholder 문구 금지",
    "자동 Merge·EC2·AWS 설정 추가 금지",
    "구현 코드·Branch·Commit을 이 문서 작업으로 만들지 않는다",
]
FORBID_BY_CAT = {
    "PAGE": ["하위 Component·API·Data 파일을 새로 만들거나 수정하지 않는다(Page 조립만)", "다른 Screen의 Page Entry를 수정하지 않는다"],
    "COMPONENT": ["Page Entry(`page.tsx`)를 만들거나 수정하지 않는다"],
    "DB": ["4개 테이블 밖의 테이블·계정·결제 테이블 추가 금지", "희망 직무(`desired_job`) 외 입력 컬럼 추가 금지(결정 D-02)", "`priority_order` 사용 로직 금지"],
    "API": ["서버 멱등키·커스텀 감사 로그 시스템 추가 금지", "요청 본문·개인정보 원문 로그 출력 금지"],
    "DATA": ["외부 데이터 연동·크롤링·공고 매칭·추천 로직 금지"],
    "LOGIC": ["MBTI 지표를 핵심 100점과 합산하는 코드 금지", "시간·난수·외부 호출에 의존하는 점수 계산 금지"],
    "E2E": ["Firefox·WebKit project 추가 금지", "외부 사이트로 실제 이동하는 검증 금지"],
    "TEST": ["운영 DB 키·실제 개인정보 사용 금지"],
    "OPS": ["자동 Merge·자동 배포·EC2·AWS 단계 금지"],
}


def load_scope(root):
    scope = {}
    for line in (root / "docs/PROJECT_SCOPE.md").read_text(encoding="utf-8").splitlines():
        m = ROW_RE.match(line)
        if m:
            cells = split_cells("|" + m.group(2) + "|")
            if cells[0] in ("IMPLEMENT", "EXCLUDED"):
                scope[m.group(1)] = {"status": cells[0], "how": cells[1] if len(cells) > 1 else "", "check": cells[2] if len(cells) > 2 else ""}
    return scope


def load_trace(root):
    req_tc, scr_ac = {}, {}
    for line in (root / "docs/UIUX_TRACEABILITY.md").read_text(encoding="utf-8").splitlines():
        m = ROW_RE.match(line)
        if m:
            cells = split_cells("|" + m.group(2) + "|")
            if len(cells) >= 6:
                req_tc[m.group(1)] = cells[5]
        m = re.match(r"^\|\s*(SCR-\d{3})\s*\|(.*)\|\s*$", line)
        if m:
            cells = split_cells("|" + m.group(2) + "|")
            if len(cells) >= 5:
                scr_ac[m.group(1)] = cells[3]
    return req_tc, scr_ac


def strip_num(s):
    return re.sub(r"^\d+\.\s*", "", s).strip()


def bullets(items, prefix="- "):
    return "\n".join(prefix + i for i in items)


def numbered(items):
    return "\n".join(f"{i}. {strip_num(x)}" for i, x in enumerate(items, 1))


def render(t, tasks, by_id, scope, req_tc, scr_ac, contract):
    dependents = [x["id"] for x in tasks if t["id"] in x["deps"]]
    reqs = t["reqs"]
    L = [f"# TASK-{t['id']} {t['title']}", "",
         f"- Task ID: {t['id']}", f"- Seq: {t['seq']}", f"- Category: {t['cat']}", f"- Priority: {t['pri']}",
         "- Status: NOT_STARTED", ""]

    def sec(name, body):
        L.extend([f"## {name}", "", body.rstrip(), ""])

    ctx = [f"{t['title']}. {ROLE[t['cat']]}"]
    ctx.append("선행 Task: " + (", ".join(f"`{d}`" for d in t["deps"]) if t["deps"] else "없음") + ".")
    ctx.append("이 Task에 의존하는 Task: " + (", ".join(f"`{d}`" for d in dependents) if dependents else "없음") + ".")
    sec("Context", "\n\n".join(ctx))

    ps = ["v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다."]
    for r in reqs:
        if r in scope:
            ps.append(f"- {r}: {scope[r]['how']}")
    if t["cat"] == "PAGE":
        ps.append("- 범위: Route Page 조립(import·상태 전환·데이터 연결)만. 하위 Component 생성은 범위가 아니다.")
    if not reqs:
        ps.append("- 이 Task는 특정 Requirement에 직접 대응하지 않는 지원 Task이며, 연결된 Task를 가능하게 하는 범위로 한정한다.")
    sec("Project Scope", "\n".join(ps))

    if reqs:
        rr = []
        for r in reqs:
            kind = r.split("-")[2]
            rr.append(f"- {r} (IMPLEMENT) — SRS {SRS_SECTION.get(kind, '')} (`docs/06_SRS_UIUX_REVISED.md`)")
        sec("Requirement Ref", "\n".join(rr))
    else:
        sec("Requirement Ref", "- 없음 (지원 Task)")

    route = f"`{t['route']}`" if t["route"] != "—" else "—"
    entry = f"`{t['entry']}`" if t["entry"] != "—" else "—"
    sec("Screen / Route / Page Entry", f"- Screen: {t['screen']}\n- Route: {route}\n- Page Entry: {entry}")

    design = DESIGN_BY_ID.get(t["id"])
    if design is None:
        if t["cat"] == "PAGE":
            sid = t["screen"]
            design = [PAGE_D, f"`{U}` {sid}", f"`{C}` {sid} (route·page_entry)"]
        else:
            design = [f"`docs/06_SRS_UIUX_REVISED.md` " + ("§6.1 Internal API Operations" if t["cat"] == "API" else "§4.2 핵심 데이터 엔터티" if t["cat"] == "DB" else ", ".join(SRS_SECTION.get(r.split("-")[2], "") for r in sorted(set(reqs))) or "관련 조항") + " — 시각 규칙 없음"]
    sec("Design Ref", bullets(design))

    sec("Depends On", bullets([f"`{d}` — {by_id[d]['title']}" for d in t["deps"]]) if t["deps"] else "- 없음")

    ef = [f"{v}: {f}" for v, f in t["files"]]
    ef.append("위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)")
    sec("Expected Files", bullets(ef))

    sec("Functional AC", numbered(segments(t["fac"])))
    sec("Visual AC", numbered(segments(t["vac"])))
    sec("Security/Privacy AC", numbered(segments(t["sac"])))

    tc = []
    for r in reqs:
        if r in req_tc and req_tc[r] and req_tc[r] != "—":
            tc.append(f"{r}: {req_tc[r]}")
    if t["cat"] == "PAGE" and t["screen"] in scr_ac:
        tc.append(f"{t['screen']}: {scr_ac[t['screen']]} (`docs/05_UIUX_APPROVED.md` §6)")
    if t["cat"] in VERIFY_CATS or t["cat"] == "E2E":
        tc.append("이 Task가 수행하는 케이스: Functional AC 각 항목")
    if not tc:
        tc.append("대응하는 SRS Test Case 없음 — 검증은 Verify의 명령·확인 항목으로 한다")
    sec("Test Cases", bullets(tc))

    sec("Verify", bullets([t["verify"]]))

    dod = ["- [ ] " + x for x in DOD_COMMON + DOD_BY_CAT.get(t["cat"], [])]
    sec("Definition of Done", "\n".join(dod))

    sec("Forbidden", bullets(FORBID_COMMON + FORBID_BY_CAT.get(t["cat"], [])))
    return "\n".join(L).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--only", nargs="*", default=[])
    a = ap.parse_args()
    root = Path(a.root).resolve()
    tdir = root / "TASKS"
    au = Audit()

    list_p = tdir / "00_TASK_LIST.md"
    if not list_p.is_file():
        print("ERROR TASKS/00_TASK_LIST.md 없음 — /gen-tasklist를 먼저 실행한다")
        return 1
    tables, _ = parse_doc(list_p.read_text(encoding="utf-8"), au)
    tasks = [x for x in (parse_task(c, au) for c in tables["tasks"]) if x]

    # ---- 사전 검사: 중복 ID, 빈 필수 열, 존재하지 않는 Depends On -----------
    ids = [x["id"] for x in tasks]
    for i in sorted({i for i in ids if ids.count(i) > 1}):
        au.err(f"중복 Task ID: {i}")
    for x in tasks:
        if x["cat"] not in CATEGORIES:
            au.err(f"{x['id']}: 알 수 없는 Category {x['cat']}")
        if x["pri"] not in PRIORITIES:
            au.err(f"{x['id']}: Priority {x['pri']}")
        for col, label in (("title", "제목"), ("fac", "Functional AC"), ("vac", "Visual AC"), ("sac", "Security/Privacy AC"),
                           ("verify", "Verify")):
            if not x[col] or x[col] in ("—", "-"):
                au.err(f"{x['id']}: 빈 필수 열 {label}")
        if not x["files"]:
            au.err(f"{x['id']}: 빈 필수 열 Expected Files")
        for d in x["deps"]:
            if d not in ids:
                au.err(f"{x['id']}: 존재하지 않는 Depends On {d}")
    if find_cycle({x["id"]: x["deps"] for x in tasks}):
        au.err("Depends On 순환")
    if au.errors:
        for e in au.errors:
            print("ERROR", e)
        print("RESULT: FAIL — 입력 검사 실패, 상세 파일을 만들지 않았다")
        return 1

    impl = [x for x in tasks if x["status"] == "IMPLEMENT"]
    skipped = [x["id"] for x in tasks if x["status"] != "IMPLEMENT"]
    by_id = {x["id"]: x for x in tasks}
    scope = load_scope(root)
    req_tc, scr_ac = load_trace(root)
    import json
    contract = json.loads((root / "design-reference/SCREEN_ROUTE_CONTRACT.json").read_text(encoding="utf-8"))

    created = updated = 0
    for x in sorted(impl, key=lambda x: int(x["seq"])):
        if a.only and x["id"] not in a.only:
            continue
        p = tdir / f"TASK-{x['id']}.md"
        existed = p.exists()
        p.write_text(render(x, tasks, by_id, scope, req_tc, scr_ac, contract), encoding="utf-8", newline="\n")
        created += not existed
        updated += existed
    print(f"구현 Task {len(impl)}개 (EXCLUDED 행 건너뜀: {skipped or '없음'}) — 생성 {created}, 갱신 {updated}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
