#!/usr/bin/env python3
"""Task 생성 전 입력 문서·계약 검증.

사용: python scripts/validate_inputs.py [--root .] [--json]
종료 코드: 0 = 통과, 1 = 오류 있음
"""
import argparse
import json
import re
import sys
from pathlib import Path

HARNESS_SCHEMA = "jobfit-screen-route-v1"
EXPECTED_SCREENS = ["SCR-001", "SCR-002", "SCR-003", "SCR-004", "SCR-005"]
CORE = {"SCR-001", "SCR-002", "SCR-003", "SCR-004"}
SUPPORTING = {"SCR-005"}

INPUT_FILES = [
    "docs/06_SRS_UIUX_REVISED.md",
    "docs/PROJECT_SCOPE.md",
    "docs/UIUX_TRACEABILITY.md",
    "design-reference/D-001/DESIGN.md",
    "design-reference/UI_CONTRACT.md",
    "design-reference/SCREEN_ROUTE_CONTRACT.json",
    "package.json",
]

D001_REQUIRED_HEADINGS = [
    "Visual Theme", "Color Token", "Typography", "Spacing", "Radius", "Shadow",
    "Header · Footer", "Search · Filter", "Form · Tabs", "Drawer · Modal",
    "Alert · Toast", "Loading · Empty · Error", "Desktop · Mobile",
    "Page Section 최대 폭", "Hero 높이", "Section별 위계",
    "화면별 Section 순서", "Placeholder 금지", "Do / Do Not",
]

REQ_RE = re.compile(r"REQ-(?:FUNC|NFR)-[A-Z]+(?:-\d{3})?")
ROW_RE = re.compile(r"^\|\s*(REQ-(?:FUNC|NFR)-[A-Z]+(?:-\d{3})?)\s*\|(.*)\|\s*$")


class Report:
    def __init__(self):
        self.errors, self.warnings, self.info = [], [], {}
        self.checks = 0

    def check(self, cond, msg):
        """검사 1건을 센다. 실패하면 오류로 기록."""
        self.checks += 1
        if not cond:
            self.errors.append(msg)
        return bool(cond)

    def err(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)


def read(root: Path, rel: str, rep: Report):
    p = root / rel
    if not p.is_file():
        rep.err(f"입력 파일 없음: {rel}")
        return None
    return p.read_text(encoding="utf-8")


def check_contract(root, rep):
    p = root / "design-reference/SCREEN_ROUTE_CONTRACT.json"
    if not p.is_file():
        return None
    try:
        c = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        rep.err(f"SCREEN_ROUTE_CONTRACT.json JSON 오류: {e}")
        return None
    if c.get("schema_version") != HARNESS_SCHEMA:
        rep.err(f"schema_version이 {HARNESS_SCHEMA}가 아님: {c.get('schema_version')}")
    if c.get("framework") != "nextjs-app-router":
        rep.err(f"framework가 nextjs-app-router가 아님: {c.get('framework')}")
    screens = c.get("screens", [])
    ids = [s.get("screen_id") for s in screens]
    if ids != EXPECTED_SCREENS:
        rep.err(f"screens가 {EXPECTED_SCREENS} 순서·개수와 다름: {ids}")
    routes = [s.get("route") for s in screens]
    entries = [s.get("page_entry") for s in screens]
    if len(set(routes)) != len(routes):
        rep.err("Route 중복")
    if len(set(entries)) != len(entries):
        rep.err("Page Entry 중복")
    for s in screens:
        sid = s.get("screen_id")
        if not s.get("page_owner_task_required"):
            rep.err(f"{sid}: page_owner_task_required가 true가 아님")
        if not s.get("preview_required"):
            rep.err(f"{sid}: preview_required가 true가 아님")
        tier = s.get("tier")
        if sid in CORE and tier != "core":
            rep.err(f"{sid}: tier가 core가 아님")
        if sid in SUPPORTING and tier != "supporting":
            rep.err(f"{sid}: tier가 supporting이 아님")
        if not str(s.get("page_entry", "")).startswith("src/app/") or not str(s.get("page_entry", "")).endswith("/page.tsx"):
            rep.err(f"{sid}: page_entry 형식 오류: {s.get('page_entry')}")
    starter = [s["screen_id"] for s in screens if s.get("starter_template_forbidden")]
    if starter != ["SCR-001"]:
        rep.err(f"starter_template_forbidden=true는 SCR-001만 가능: {starter}")
    tech = c.get("technical_routes", [])
    if any(t.get("counts_as_screen") for t in tech):
        rep.err("technical_routes 중 Screen으로 계산되는 항목이 있음")
    kinds = {t.get("kind") for t in tech}
    for need in ("api", "not-found", "redirect"):
        if need not in kinds:
            rep.err(f"technical_routes에 {need} 항목 없음")
    nav = c.get("required_navigation", [])
    if not nav:
        rep.err("required_navigation이 비어 있음")
    rep.info["screens"] = [
        {"id": s["screen_id"], "route": s["route"], "page_entry": s["page_entry"], "tier": s["tier"]}
        for s in screens
    ]
    rep.info["technical_entries"] = [t["entry"] for t in tech if "entry" in t]
    return c


def parse_scope_statuses(text):
    """PROJECT_SCOPE §4 표에서 {REQ: IMPLEMENT|EXCLUDED}."""
    out = {}
    for line in text.splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        cells = [c.strip() for c in m.group(2).split("|")]
        if cells and cells[0] in ("IMPLEMENT", "EXCLUDED"):
            out[m.group(1)] = cells[0]
    return out


def parse_trace_statuses(text):
    out = {}
    for line in text.splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        cells = [c.strip() for c in m.group(2).split("|")]
        if cells and cells[0] in ("NOT_IMPLEMENTED", "EXCLUDED", "IMPLEMENTED"):
            out[m.group(1)] = cells[0]
    return out


def check_requirements(root, rep):
    scope = read(root, "docs/PROJECT_SCOPE.md", rep)
    trace = read(root, "docs/UIUX_TRACEABILITY.md", rep)
    srs = read(root, "docs/06_SRS_UIUX_REVISED.md", rep)
    if scope is None or trace is None or srs is None:
        return {}
    statuses = parse_scope_statuses(scope)
    if not statuses:
        rep.err("PROJECT_SCOPE.md에서 Requirement 상태를 읽지 못함")
        return {}
    trace_st = parse_trace_statuses(trace)
    srs_ids = set(REQ_RE.findall(srs))
    for rid, st in statuses.items():
        if rid not in srs_ids:
            rep.err(f"{rid}: 06_SRS_UIUX_REVISED.md에 없음")
        t = trace_st.get(rid)
        if t is None:
            rep.err(f"{rid}: UIUX_TRACEABILITY.md에 없음")
        elif (st == "EXCLUDED") != (t == "EXCLUDED"):
            rep.err(f"{rid}: PROJECT_SCOPE({st})와 Traceability({t}) 상태 불일치")
    for rid in trace_st:
        if rid not in statuses:
            rep.err(f"{rid}: Traceability에는 있으나 PROJECT_SCOPE에 없음")
    # 구현됐다는 거짓 기록 방지
    if any(v == "IMPLEMENTED" for v in trace_st.values()):
        rep.warn("Traceability에 IMPLEMENTED 항목이 있음 — 실제 코드와 대조 필요")
    n_impl = sum(1 for v in statuses.values() if v == "IMPLEMENT")
    n_excl = sum(1 for v in statuses.values() if v == "EXCLUDED")
    rep.info["requirements"] = {"total": len(statuses), "IMPLEMENT": n_impl, "EXCLUDED": n_excl}
    return statuses


def check_design(root, rep):
    text = read(root, "design-reference/D-001/DESIGN.md", rep)
    if text is None:
        return
    heads = [l for l in text.splitlines() if l.startswith("## ")]
    joined = "\n".join(heads)
    for h in D001_REQUIRED_HEADINGS:
        if h not in joined:
            rep.err(f"D-001/DESIGN.md에 '{h}' 섹션 없음")
    manifest = root / "design-reference/DESIGN_MANIFEST.md"
    if manifest.is_file():
        m = manifest.read_text(encoding="utf-8")
        if "LOCKED" not in m or "D-001" not in m:
            rep.err("DESIGN_MANIFEST.md가 D-001 LOCKED 상태가 아님")
    else:
        rep.warn("DESIGN_MANIFEST.md 없음")


def check_ui_contract(root, contract, rep):
    text = read(root, "design-reference/UI_CONTRACT.md", rep)
    if text is None or not contract:
        return
    for s in contract.get("screens", []):
        if f"## {s['screen_id']}" not in text:
            rep.err(f"UI_CONTRACT.md에 {s['screen_id']} 섹션 없음")
        if s["route"] not in text:
            rep.err(f"UI_CONTRACT.md에 {s['route']} 없음")
        if s["page_entry"] not in text:
            rep.err(f"UI_CONTRACT.md에 {s['page_entry']} 없음")


def check_package_and_tree(root, contract, rep):
    p = root / "package.json"
    if p.is_file():
        try:
            pkg = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            rep.err(f"package.json JSON 오류: {e}")
            pkg = {}
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        rep.info["package"] = {
            "next": deps.get("next"),
            "react": deps.get("react"),
            "scripts": sorted(pkg.get("scripts", {})),
            "playwright": "@playwright/test" in deps or "playwright" in deps,
        }
        if "next" not in deps:
            rep.err("package.json에 next 의존성 없음")
    app = root / "src/app"
    if not app.is_dir():
        rep.err("src/app 디렉터리 없음")
        return
    tree = sorted(str(f.relative_to(root)).replace("\\", "/") for f in app.rglob("*") if f.is_file())
    rep.info["src_app_tree"] = tree
    if contract:
        existing = []
        for s in contract.get("screens", []):
            if s["page_entry"] in tree:
                existing.append(s["page_entry"])
        rep.info["existing_page_entries"] = existing
    page = root / "src/app/page.tsx"
    if page.is_file():
        t = page.read_text(encoding="utf-8")
        rep.info["root_page_is_starter"] = ("next.svg" in t) or ("To get started" in t)
    else:
        rep.info["root_page_is_starter"] = None
    src_dirs = [d for d in ("src/components", "src/data", "src/lib", "tests") if (root / d).exists()]
    rep.info["existing_support_dirs"] = src_dirs


EXPECTED_ROUTES = ["/diagnosis", "/diagnosis/result", "/diagnosis/result/recommendations",
                   "/diagnosis/result/jobs", "/diagnosis/attitude"]
EXPECTED_FUNC, EXPECTED_NFR = 16, 8
PAGE_ENTRY_RE = re.compile(r"^src/app/(?:[A-Za-z0-9_\-\[\]\(\)]+/)*page\.tsx$")
SPEC_DOCS = ["docs/01_PRD.md", "docs/06_SRS_UIUX_REVISED.md", "docs/PROJECT_SCOPE.md",
             "docs/UIUX_TRACEABILITY.md", "design-reference/UI_CONTRACT.md"]
INACTIVE_RE = re.compile(r"제외|금지|않|범위 ?밖|Post-MVP|OS-\d|EXCLUDED|하지|NOT|not|Out of Scope")


def check_spec(root, rep):
    """요구된 11개 검사 항목. 개별 검사마다 개수를 센다."""
    # 1. Next.js 의존성
    pkg = {}
    pj = root / "package.json"
    if rep.check(pj.is_file(), "누락 파일: package.json"):
        try:
            pkg = json.loads(pj.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            rep.err(f"package.json JSON 오류: {e}")
    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
    rep.check("next" in deps, "package.json에 next 의존성 없음")
    # 2. 루트 page·layout
    for rel in ("src/app/page.tsx", "src/app/layout.tsx"):
        rep.check((root / rel).is_file(), f"누락 파일: {rel}")
    # 3. PRD·SRS·Scope·UI 문서
    for rel in SPEC_DOCS:
        rep.check((root / rel).is_file(), f"누락 파일: {rel}")
    # 4. D-001 DESIGN.md, LOCKED Manifest
    rep.check((root / "design-reference/D-001/DESIGN.md").is_file(), "누락 파일: design-reference/D-001/DESIGN.md")
    mf = root / "design-reference/DESIGN_MANIFEST.md"
    if rep.check(mf.is_file(), "누락 파일: design-reference/DESIGN_MANIFEST.md"):
        rep.check(re.search(r"\*\*Status\*\*\s*\|\s*LOCKED", mf.read_text(encoding="utf-8")) is not None,
                  "DESIGN_MANIFEST.md Status가 LOCKED가 아님")
    # 5~9. SCREEN_ROUTE_CONTRACT.json
    cp = root / "design-reference/SCREEN_ROUTE_CONTRACT.json"
    contract = None
    if rep.check(cp.is_file(), "누락 파일: design-reference/SCREEN_ROUTE_CONTRACT.json"):
        try:
            contract = json.loads(cp.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            rep.err(f"SCREEN_ROUTE_CONTRACT.json JSON 오류: {e}")
        rep.check(contract is not None, "SCREEN_ROUTE_CONTRACT.json 파싱 실패")
    if contract is not None:
        screens = contract.get("screens", [])
        rep.check(len(screens) == 5, f"Screen 수가 5개가 아님: {len(screens)}")
        have = {s.get("screen_id") for s in screens}
        for sid in EXPECTED_SCREENS:
            rep.check(sid in have, f"누락 Screen: {sid}")
        routes = [s.get("route") for s in screens]
        for r in EXPECTED_ROUTES:
            rep.check(r in routes, f"누락 Route: {r}")
        for r in routes:
            rep.check(r in EXPECTED_ROUTES, f"허용되지 않은 Route: {r}")
        for s in screens:
            pe = str(s.get("page_entry", ""))
            rep.check(PAGE_ENTRY_RE.match(pe) is not None,
                      f"{s.get('screen_id')}: Page Entry 형식 오류: {pe}")
    # 10. PROJECT_SCOPE의 REQ-FUNC / REQ-NFR 전체 등장
    scope_p = root / "docs/PROJECT_SCOPE.md"
    srs_p = root / "docs/06_SRS_UIUX_REVISED.md"
    if scope_p.is_file():
        scope_ids = set(parse_scope_statuses(scope_p.read_text(encoding="utf-8")))  # §4 표의 Requirement 행
        func = {i for i in scope_ids if i.startswith("REQ-FUNC")}
        nfr = {i for i in scope_ids if i.startswith("REQ-NFR")}
        rep.check(len(func) == EXPECTED_FUNC, f"REQ-FUNC {EXPECTED_FUNC}개 기대, PROJECT_SCOPE에는 {len(func)}개")
        rep.check(len(nfr) == EXPECTED_NFR, f"REQ-NFR {EXPECTED_NFR}개 기대, PROJECT_SCOPE에는 {len(nfr)}개")
        if srs_p.is_file():
            srs_ids = {i for i in REQ_RE.findall(srs_p.read_text(encoding="utf-8")) if i[-3:].isdigit()}
            for rid in sorted(srs_ids - scope_ids):
                rep.check(False, f"PROJECT_SCOPE에 누락된 Requirement: {rid}")
    # 11. AWS·EC2가 활성 기술로 정의되지 않음
    for rel in SPEC_DOCS:
        p = root / rel
        if not p.is_file():
            continue
        bad = [n for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1)
               if re.search(r"AWS|EC2", line) and not INACTIVE_RE.search(line)]
        rep.check(not bad, f"AWS·EC2가 활성 기술로 정의됨: {rel}:{bad}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--json", action="store_true", help="결과를 JSON으로 출력")
    a = ap.parse_args()
    root = Path(a.root).resolve()
    rep = Report()

    for rel in INPUT_FILES:
        if not (root / rel).is_file():
            rep.err(f"입력 파일 없음: {rel}")
    contract = check_contract(root, rep)
    check_requirements(root, rep)
    check_design(root, rep)
    check_ui_contract(root, contract, rep)
    check_package_and_tree(root, contract, rep)
    check_spec(root, rep)

    ok = not rep.errors
    if a.json:
        print(json.dumps({"ok": ok, "errors": rep.errors, "warnings": rep.warnings, "info": rep.info},
                         ensure_ascii=False, indent=2))
    else:
        print(f"HARNESS_SCHEMA: {HARNESS_SCHEMA}")
        r = rep.info.get("requirements")
        if r:
            print(f"Requirement: {r['total']}개 (IMPLEMENT {r['IMPLEMENT']}, EXCLUDED {r['EXCLUDED']})")
        for s in rep.info.get("screens", []):
            print(f"  {s['id']} [{s['tier']}] {s['route']} -> {s['page_entry']}")
        print(f"src/app 파일: {len(rep.info.get('src_app_tree', []))}개, 스타터 root page: {rep.info.get('root_page_is_starter')}")
        for w in rep.warnings:
            print(f"WARN  {w}")
        for e in rep.errors:
            print(f"ERROR {e}")
        print("RESULT:", "PASS" if ok else f"FAIL ({len(rep.errors)} errors)")
        if ok:
            print(f"VALIDATE_INPUTS_PASS checks={rep.checks}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
