#!/usr/bin/env python3
"""Task 의존성(DAG)을 읽어 Wave 계획을 만든다.

사용: python scripts/build_waves.py [--root .] [--max-per-wave 7] [--force]
입력: TASKS/TASK_MANIFEST.csv, TASKS/TASK-<ID>.md(Depends On 절), design-reference/SCREEN_ROUTE_CONTRACT.json
출력: TASKS/TASK_DAG.md, TASKS/WAVE_PLAN.md, TASKS/WAVE_STATE.json, TASK_MANIFEST.csv의 wave_id 열
실패하면(순환·선행 Task가 뒤 Wave·입력 불일치) 아무 파일도 쓰지 않고 exit 1.
이미 진행 중인 WAVE_STATE.json(pending이 아닌 Wave)이 있으면 --force 없이는 덮어쓰지 않는다.
Branch·PR·Merge·자동 수정은 하지 않는다.
"""
import argparse
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    sys.stdout.reconfigure(errors="replace")
except Exception:
    pass

SCHEMA = "jobfit-wave-v1"

# (그룹 키, 제목, Task ID 정규식). 위에서부터 처음 맞는 그룹에 배치한다. 그룹 순서가 Wave 순서다.
GROUPS = [
    ("scaffold", "Scaffold·테스트 도구·Harness 확인", r"FND-TEST-TOOLING"),
    ("common", "공통 UI(Token·Layout·Feedback·Section)·정적 데이터", r"FND-.*|DATA-.*"),
    ("logic-db", "진단 로직·Supabase 4개 Table·기본 RLS", r"LIB-.*|DB-.*"),
    ("scr001", "SCR-001 진단 입력(API·Component·Page Owner)", r"API-DIAG-SUBMIT|FEAT-OBS-EVENTS|CMP-FIELDS|CMP-DIAG-FORM|PAGE-SCR001"),
    ("scr002", "SCR-002 역량리포트(API·Component·Page Owner)", r"API-DIAG-RESULT|API-DIAG-REASONS|CMP-SCORE-HERO|CMP-REASON-DRAWER|CMP-DEDUCTION-CHIPS|PAGE-SCR002"),
    ("scr003", "SCR-003 직업훈련 추천(API·Component·Page Owner)", r"API-DIAG-RECOMMENDATIONS|CMP-RECO-GRID|PAGE-SCR003"),
    ("scr004", "SCR-004 직무추천(API·Component·Page Owner)", r"API-DIAG-JOBS|CMP-JOB-SITES|PAGE-SCR004"),
    ("scr005", "SCR-005 직무수행태도 진단(API·Component·Page Owner)", r"API-ATTITUDE|CMP-MBTI-GRID|CMP-ATTITUDE-PANEL|PAGE-SCR005"),
    ("verify", "Unit·Playwright Chromium·CI", r"UNIT-.*|TEST-.*|E2E-.*|OPS-CI"),
    ("release", "Vercel Preview·수동 확인·Release 확인", r"MANUAL-.*|OPS-VERCEL-DB-CHECK|RELEASE-CHECK"),
]

errors = []


def fail(msg):
    errors.append(msg)


def read_manifest(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        return rd.fieldnames, list(rd)


def split(v):
    return [x for x in (v or "").split(";") if x]


def detail_deps(root, tid):
    p = root / "TASKS" / f"TASK-{tid}.md"
    if not p.is_file():
        p = root / "TASKS" / "details" / f"TASK-{tid}.md"
    if not p.is_file():
        return None
    m = re.search(r"^## Depends On\s*\n(.*?)(?=^## |\Z)", p.read_text(encoding="utf-8"), re.S | re.M)
    if not m:
        return None
    return re.findall(r"^- `([A-Z0-9-]+)`", m.group(1), re.M)


def find_cycles(deps):
    """Tarjan SCC. 크기 2 이상이거나 자기 참조인 성분을 순환으로 센다."""
    index, low, on, stack, out = {}, {}, set(), [], []
    counter = [0]

    def visit(v):
        index[v] = low[v] = counter[0]
        counter[0] += 1
        stack.append(v)
        on.add(v)
        for w in deps[v]:
            if w not in deps:
                continue
            if w not in index:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            comp = []
            while True:
                w = stack.pop()
                on.discard(w)
                comp.append(w)
                if w == v:
                    break
            if len(comp) > 1 or v in deps[v]:
                out.append(sorted(comp))

    sys.setrecursionlimit(10000)
    for v in sorted(deps):
        if v not in index:
            visit(v)
    return out


def topo_group(ids, deps, page_owners):
    """그룹 안 위상 정렬. 같은 순위에서는 Page Owner를 뒤로, 그 안에서는 Task ID 순."""
    left, done, order = set(ids), set(), []
    while left:
        ready = sorted((t for t in left if all(d in done or d not in left for d in deps[t])),
                       key=lambda t: (t in page_owners, t))
        if not ready:
            fail(f"그룹 안 위상 정렬 실패: {sorted(left)}")
            break
        t = ready[0]
        order.append(t)
        left.discard(t)
        done.add(t)
    return order


def modify_targets(files):
    out = set()
    for item in files:
        verb, _, path = item.partition(" ")
        if verb == "modify":
            out.add(path)
    return out


def level_of(tid, deps, memo):
    if tid not in memo:
        memo[tid] = 0 if not deps[tid] else 1 + max(level_of(d, deps, memo) for d in deps[tid])
    return memo[tid]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--max-per-wave", type=int, default=7)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    tdir = root / "TASKS"

    # ---- 입력 ----
    mpath = tdir / "TASK_MANIFEST.csv"
    cpath = root / "design-reference/SCREEN_ROUTE_CONTRACT.json"
    if not mpath.is_file() or not cpath.is_file():
        print(f"입력 없음: {mpath if not mpath.is_file() else cpath}")
        return 1
    fields, rows = read_manifest(mpath)
    contract = json.loads(cpath.read_text(encoding="utf-8"))
    tasks = {r["Task ID"]: r for r in rows}
    if len(tasks) != len(rows):
        fail("TASK_MANIFEST.csv에 중복 Task ID가 있다")
    deps = {tid: split(r["Depends On"]) for tid, r in tasks.items()}
    files = {tid: split(r["Expected Files"]) for tid, r in tasks.items()}

    # ---- dependency 검증: 상세 파일과 Manifest 일치, 존재하지 않는 선행 Task ----
    for tid, ds in deps.items():
        for d in ds:
            if d not in tasks:
                fail(f"{tid}: 존재하지 않는 선행 Task {d}")
        dd = detail_deps(root, tid)
        if dd is None:
            fail(f"{tid}: 상세 파일 또는 Depends On 절이 없다")
        elif sorted(dd) != sorted(ds):
            fail(f"{tid}: 상세 Depends On {sorted(dd)} 과 Manifest {sorted(ds)} 불일치")

    # ---- 규칙 1: 순환 ----
    cycles = find_cycles(deps)
    for c in cycles:
        fail(f"순환 의존성: {' -> '.join(c)}")

    # ---- Page Owner: Contract의 page_entry와 같은 Page Entry를 가진 Task ----
    page_owners = {}
    for s in contract["screens"]:
        owners = [tid for tid, r in tasks.items() if r["Page Entry"] == s["page_entry"]]
        if len(owners) != 1:
            fail(f"{s['screen_id']}: Page Owner Task가 {len(owners)}개({owners})")
        else:
            page_owners[owners[0]] = s["screen_id"]

    # ---- 그룹 배정 ----
    group_of = {}
    for tid in sorted(tasks):
        hit = [g for g in GROUPS if re.fullmatch(g[2], tid)]
        if not hit:
            fail(f"{tid}: 어느 Wave 그룹에도 속하지 않음(GROUPS 갱신 필요)")
        else:
            group_of[tid] = hit[0][0]
    if errors:
        return report_fail()

    # ---- Wave 구성: 그룹 순서대로, 위상 정렬 후 크기·파일 충돌 기준으로 끊는다 ----
    waves = []
    for gkey, gtitle, _ in GROUPS:
        ids = [t for t in tasks if group_of[t] == gkey]
        if not ids:
            continue
        order = topo_group(ids, deps, page_owners)
        k = -(-len(order) // args.max_per_wave)
        target = -(-len(order) // k)  # 같은 그룹을 나눌 때 크기를 고르게
        chunks, cur, cur_mod = [], [], set()
        for t in order:
            mod = modify_targets(files[t])
            if cur and (len(cur) >= target or (mod & cur_mod)):
                chunks.append(cur)
                cur, cur_mod = [], set()
            cur.append(t)
            cur_mod |= mod
        if cur:
            chunks.append(cur)
        for i, ch in enumerate(chunks, 1):
            title = gtitle if len(chunks) == 1 else f"{gtitle} ({i}/{len(chunks)})"
            waves.append({"group": gkey, "title": title, "task_ids": ch})
    for i, w in enumerate(waves, 1):
        w["wave_id"] = f"W{i:02d}"
    wave_of = {t: w["wave_id"] for w in waves for t in w["task_ids"]}
    pos = {t: (wi, ti) for wi, w in enumerate(waves) for ti, t in enumerate(w["task_ids"])}

    # ---- 규칙 2: 선행 Task가 뒤에 배치되면 실패 / Page Owner는 Wave의 마지막 통합 Task ----
    for t, ds in deps.items():
        for d in ds:
            if pos[d] >= pos[t]:
                fail(f"{t}({wave_of[t]})의 선행 {d}({wave_of[d]})가 같거나 뒤에 배치됨")
    for t, scr in page_owners.items():
        w = waves[pos[t][0]]
        if w["task_ids"][-1] != t:
            fail(f"{t}({scr}): Page Owner가 {w['wave_id']}의 마지막 Task가 아님")
        for o, ds in deps.items():
            if t in ds and wave_of[o] == wave_of[t] and pos[o] < pos[t]:
                fail(f"{o}가 Page Owner {t}보다 앞인데 의존함")
    # 규칙 5: 같은 Wave 안 modify 대상 중복 금지
    for w in waves:
        seen = {}
        for t in w["task_ids"]:
            for f in modify_targets(files[t]):
                if f in seen:
                    fail(f"{w['wave_id']}: {seen[f]}와 {t}가 같은 파일 {f}를 modify함")
                seen[f] = t
    if errors:
        return report_fail()

    # ---- 진행 중 상태 보호 ----
    spath = tdir / "WAVE_STATE.json"
    if spath.is_file() and not args.force:
        try:
            old = json.loads(spath.read_text(encoding="utf-8"))
            busy = [w.get("wave_id") for w in old.get("waves", []) if w.get("status") not in (None, "pending")]
        except (json.JSONDecodeError, AttributeError):
            busy = ["(읽을 수 없는 기존 파일)"]
        if busy:
            print(f"기존 WAVE_STATE.json에 진행 기록이 있어 덮어쓰지 않음: {busy}. 덮어쓰려면 --force")
            return 1

    # ---- 출력 ----
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    memo = {}
    level = {t: level_of(t, deps, memo) for t in tasks}

    state = {
        "schema_version": SCHEMA,
        "generated_at": now,
        "waves": [{
            "wave_id": w["wave_id"], "title": w["title"], "task_ids": w["task_ids"], "status": "pending",
            "checkpoint_required": any(t in page_owners for t in w["task_ids"]) or "MANUAL-PREVIEW" in w["task_ids"],
            "checkpoint_result": None,
        } for w in waves],
        "tasks": {t: {"wave_id": wave_of[t], "status": "pending"} for w in waves for t in w["task_ids"]},
    }
    spath.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    L = ["# TASK_DAG", "",
         f"`scripts/build_waves.py`가 `TASK_MANIFEST.csv`와 `TASK-*.md`의 Depends On에서 만든 파일이다(생성 {now}). 직접 고치지 않는다.", "",
         f"- Task {len(tasks)}개, 의존 간선 {sum(len(v) for v in deps.values())}개, 순환 의존성 0개",
         f"- 최장 의존 경로 깊이 {max(level.values())}", "",
         "## Task별 의존", "", "| Task | Wave | 깊이 | Depends On |", "|---|---|---|---|"]
    for w in waves:
        for t in w["task_ids"]:
            L.append(f"| `{t}` | {w['wave_id']} | {level[t]} | {', '.join(f'`{d}`({wave_of[d]})' for d in deps[t]) or '-'} |")
    edges = sorted({(wave_of[d], wave_of[t]) for t, ds in deps.items() for d in ds if wave_of[d] != wave_of[t]})
    L += ["", "## Wave 간 의존", "", "```mermaid", "flowchart LR"]
    L += [f'  {w["wave_id"]}["{w["wave_id"]}"]' for w in waves]
    L += [f"  {a} --> {b}" for a, b in edges]
    L += ["```", ""]
    (tdir / "TASK_DAG.md").write_text("\n".join(L), encoding="utf-8")

    P = ["# WAVE_PLAN", "",
         f"`scripts/build_waves.py`가 만든 Wave 계획이다(생성 {now}, 스키마 {SCHEMA}). Wave ID는 이 파일과 `WAVE_STATE.json`이 정본이다.", "",
         "## 규칙", "",
         f"- Wave당 최대 {args.max_per_wave}개 Task. 한 그룹이 더 크거나 같은 파일을 `modify`하는 Task가 있으면 같은 그룹을 여러 Wave로 나눈다.",
         "- 한 Wave 안에서는 선행 Task가 먼저 오는 순서(같은 순위는 Task ID 순)로 하나씩 실행한다. Page Owner는 그 Wave의 마지막이다.",
         "- 선행 Task는 항상 앞선 Wave 또는 같은 Wave의 앞 순서에 있다.",
         "- `checkpoint_required`가 true인 Wave는 끝나면 사람이 Desktop·Mobile Preview를 확인한다.",
         "- 자동 Branch·PR·Merge와 자동 수정 재시도는 없다.", "",
         "## Wave 요약", "", "| Wave | 제목 | Task 수 | Checkpoint |", "|---|---|---|---|"]
    for w, sw in zip(waves, state["waves"]):
        P.append(f"| {w['wave_id']} | {w['title']} | {len(w['task_ids'])} | {'필요' if sw['checkpoint_required'] else '-'} |")
    for w, sw in zip(waves, state["waves"]):
        P += ["", f"## {w['wave_id']} {w['title']}", ""]
        for i, t in enumerate(w["task_ids"], 1):
            tag = f" — Page Owner({page_owners[t]})" if t in page_owners else ""
            P.append(f"{i}. `{t}` {tasks[t]['제목']}{tag}")
        P.append("")
        P.append(f"Checkpoint: {'필요(사람이 Preview 확인)' if sw['checkpoint_required'] else '없음'}")
    P.append("")
    (tdir / "WAVE_PLAN.md").write_text("\n".join(P), encoding="utf-8")

    out_fields = [f for f in fields if f != "wave_id"] + ["wave_id"]
    with mpath.open("w", encoding="utf-8-sig", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=out_fields)
        wr.writeheader()
        for r in rows:
            r["wave_id"] = wave_of[r["Task ID"]]
            wr.writerow(r)

    # ---- 종료 출력 ----
    print(f"순환 의존성: 0개")
    print(f"Wave {len(waves)}개, Task {len(tasks)}개")
    for w in waves:
        note = "" if 4 <= len(w["task_ids"]) <= 7 else "  (4~7개 범위 밖: 그룹 크기 때문)"
        print(f"  {w['wave_id']} {len(w['task_ids']):>2}개  {w['title']}{note}")
    print("Page Owner 위치:")
    for t, scr in sorted(page_owners.items(), key=lambda x: x[1]):
        w = waves[pos[t][0]]
        print(f"  {scr} {t}: {w['wave_id']} {pos[t][1] + 1}/{len(w['task_ids'])}번째(마지막)")
    print("BUILD_WAVES_PASS")
    return 0


def report_fail():
    for e in errors:
        print(f"ERROR {e}")
    print(f"BUILD_WAVES_FAIL ({len(errors)} errors)")
    return 1


if __name__ == "__main__":
    sys.exit(main() if not errors else report_fail())
