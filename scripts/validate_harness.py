#!/usr/bin/env python3
"""Claude Code 하네스(CLAUDE.md·Skill·Command) 검증.

사용: python scripts/validate_harness.py [--root .]
성공: VALIDATE_HARNESS_PASS checks=N 출력, exit 0
실패: "파일: 누락 규칙" 형식으로 출력, exit 1
파일을 수정하지 않는다.
"""
import argparse
import json
import re
import sys
from pathlib import Path

CLAUDE = "CLAUDE.md"
SKILL = ".claude/skills/jobfit-project-pipeline/SKILL.md"
SKILL_NAME = "jobfit-project-pipeline"
COMMANDS = ["gen-tasklist", "gen-task-details", "audit-tasks", "prepare-task", "implement-task", "run-wave", "release-check"]
CONTRACT = "design-reference/SCREEN_ROUTE_CONTRACT.json"
DESIGN = "design-reference/D-001/DESIGN.md"
SCOPE = "docs/PROJECT_SCOPE.md"
MARKERS = {
    "HARNESS_SCHEMA": "jobfit-screen-route-v1",
    "DESIGN_PATH": DESIGN,
    "SCREEN_CONTRACT": CONTRACT,
    "PROJECT_SCOPE": SCOPE,
    "PLAYWRIGHT_ENABLED": "true",
    "PLAYWRIGHT_SCOPE": "chromium-core-flows",
    "AUTO_MERGE": "false",
    "AWS_ENABLED": "false",
}
TABLES = ["diagnosis_inputs", "diagnosis_results", "deduction_items", "recommendation_items"]
EXCLUDED_IDS = ["REQ-FUNC-PERSONALIZE-001~003", "REQ-FUNC-ADMIN", "REQ-NFR-AVAIL-001", "REQ-NFR-PRIV-002"]

errors = []
checks = []


def err(path, rule):
    errors.append(f"{path}: {rule}")


def read(root, rel):
    p = root / rel
    return p.read_text(encoding="utf-8") if p.is_file() else None


def need(text, path, rules):
    """text 안에 각 규칙(문자열 또는 정규식 튜플)이 있어야 한다."""
    if text is None:
        return
    for rule in rules:
        label, pat = rule if isinstance(rule, tuple) else (rule, re.escape(rule))
        if not re.search(pat, text):
            err(path, f"누락 규칙 — {label}")


def check(num, title):
    def deco(fn):
        checks.append((num, title, fn))
        return fn
    return deco


def parse_markers(text):
    out = {}
    for line in (text or "").splitlines():
        m = re.match(r"^([A-Z][A-Z0-9_]+)=(.*)$", line.strip())
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---", (text or "").replace("\r\n", "\n"), re.S)
    return dict(re.findall(r"^([a-z-]+):\s*(.*)$", m.group(1), re.M)) if m else {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    root = Path(ap.parse_args().root).resolve()
    claude = read(root, CLAUDE)
    skill = read(root, SKILL)
    markers = parse_markers(claude)
    contract = None
    cp = root / CONTRACT
    if cp.is_file():
        try:
            contract = json.loads(cp.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            err(CONTRACT, f"JSON 오류 — {e}")

    @check(1, "CLAUDE.md 존재")
    def _():
        if claude is None:
            err(CLAUDE, "파일 없음")
        else:
            need(claude, CLAUDE, ["Harness Marker"])

    @check(2, "Claude Code Skill 파일 존재")
    def _():
        if skill is None:
            err(SKILL, "파일 없음")
            return
        fm = frontmatter(skill)
        if fm.get("name") != SKILL_NAME:
            err(SKILL, f"frontmatter name이 {SKILL_NAME}가 아님({fm.get('name')})")
        if not fm.get("description"):
            err(SKILL, "frontmatter description 없음")

    @check(3, "7개 Command 존재")
    def _():
        for c in COMMANDS:
            rel = f".claude/commands/{c}.md"
            t = read(root, rel)
            if t is None:
                err(rel, "파일 없음")
                continue
            if not frontmatter(t).get("description"):
                err(rel, "frontmatter description 없음")
            need(t, rel, [SKILL_NAME])
        extra = sorted(p.stem for p in (root / ".claude/commands").glob("*.md") if p.stem not in COMMANDS) \
            if (root / ".claude/commands").is_dir() else []
        for e in extra:
            err(f".claude/commands/{e}.md", f"예상한 7개 Command에 없는 파일(검증 목록 갱신 필요)")

    @check(4, "jobfit-screen-route-v1 Marker 존재(8개 Marker)")
    def _():
        for k, v in MARKERS.items():
            if k not in markers:
                err(CLAUDE, f"누락 Marker — {k}")
            elif k not in ("AUTO_MERGE", "AWS_ENABLED") and markers[k] != v:
                err(CLAUDE, f"Marker 값 불일치 — {k}={markers[k]} (기대 {v})")
        if contract and contract.get("schema_version") != MARKERS["HARNESS_SCHEMA"]:
            err(CONTRACT, f"schema_version이 {MARKERS['HARNESS_SCHEMA']}가 아님({contract.get('schema_version')})")
        need(skill, SKILL, [MARKERS["HARNESS_SCHEMA"]])

    @check(5, "D-001 DESIGN 경로 일치")
    def _():
        if markers.get("DESIGN_PATH") != DESIGN:
            err(CLAUDE, f"DESIGN_PATH가 {DESIGN}가 아님({markers.get('DESIGN_PATH')})")
        if not (root / DESIGN).is_file():
            err(DESIGN, "파일 없음")
        manifest = read(root, "design-reference/DESIGN_MANIFEST.md")
        if manifest is None:
            err("design-reference/DESIGN_MANIFEST.md", "파일 없음")
        elif not re.search(r"\*\*Status\*\*\s*\|\s*LOCKED", manifest) or DESIGN not in manifest:
            err("design-reference/DESIGN_MANIFEST.md", f"Active File {DESIGN}·Status LOCKED 아님")
        need(claude, CLAUDE, [DESIGN])

    @check(6, "Screen Contract 경로 일치")
    def _():
        if markers.get("SCREEN_CONTRACT") != CONTRACT:
            err(CLAUDE, f"SCREEN_CONTRACT가 {CONTRACT}가 아님({markers.get('SCREEN_CONTRACT')})")
        if not cp.is_file():
            err(CONTRACT, "파일 없음")
        if markers.get("PROJECT_SCOPE") != SCOPE or not (root / SCOPE).is_file():
            err(CLAUDE, f"PROJECT_SCOPE가 {SCOPE}와 다르거나 파일이 없음")
        need(claude, CLAUDE, [CONTRACT])

    @check(7, "Page Owner 5개 규칙 존재")
    def _():
        if not contract:
            return
        screens = contract.get("screens", [])
        if len(screens) != 5:
            err(CONTRACT, f"Screen이 5개가 아님({len(screens)})")
        for s in screens:
            for key in ("page_entry", "route"):
                if s[key] not in (claude or ""):
                    err(CLAUDE, f"누락 규칙 — {s['screen_id']} {s[key]}")
            if s["page_entry"] not in (skill or ""):
                err(SKILL, f"누락 규칙 — {s['screen_id']} {s['page_entry']}")
        need(claude, CLAUDE, ["Page Owner", ("Page Entry에서 Component를 실제로 조립", r"Page Entry에서 Component를 실제로 조립"),
                              ("한 Task가 여러 Page Entry를 소유하지 않는다", r"여러 Page Entry를 소유하지 않는다"), "Starter"])
        need(skill, SKILL, ["Page Owner", ("Screen마다 정확히 하나", r"정확히 하나"), "Route Page 조립만"])

    @check(8, "DB Table 4개 기본 범위 존재")
    def _():
        need(claude, CLAUDE, TABLES + [("4개 테이블", r"4개 테이블")])
        need(skill, SKILL, TABLES + [("4개 테이블", r"4개 테이블")])

    @check(9, "외부 입력 비저장 규칙 존재")
    def _():
        need(claude, CLAUDE, [
            ("POST /api/diagnosis로만 서버 전송", r"POST /api/diagnosis"),
            ("URL·로그·분석·외부 사이트로 보내지 않음", r"URL 쿼리·콘솔 로그·분석 이벤트·외부 사이트로 보내지 않는다"),
            ("외부 사이트에는 희망 직무 검색어만", r"희망 직무 검색어만"),
            ("이동·클릭 기록 비저장", r"이동·클릭 기록은 저장하지 않는다"),
            ("sessionStorage에는 result_id만", r"`result_id`만 `sessionStorage`"),
        ])
        need(skill, SKILL, ["외부 입력 비저장 불변조건", ("이동·클릭 기록을 서버·DB에 저장하지 않는다", r"클릭 기록을 서버·DB에 저장하지 않는다")])

    @check(10, "Playwright Chromium 규칙 존재")
    def _():
        need(claude, CLAUDE, [("Chromium project 하나", r"Chromium project 하나"), ("Firefox·WebKit 없음", r"Firefox·WebKit")])
        need(skill, SKILL, [("Playwright project는 chromium 하나", r"`chromium` 하나"), ("Smoke Task", r"Smoke"), "E2E-PUBLIC-SMOKE"])

    @check(11, "AUTO_MERGE=false")
    def _():
        if markers.get("AUTO_MERGE") != "false":
            err(CLAUDE, f"AUTO_MERGE가 false가 아님({markers.get('AUTO_MERGE')})")
        need(claude, CLAUDE, [("자동 PR·자동 Merge 금지 규칙", r"자동 PR·자동 Merge를 실행하지 않는다")])

    @check(12, "AWS_ENABLED=false")
    def _():
        if markers.get("AWS_ENABLED") != "false":
            err(CLAUDE, f"AWS_ENABLED가 false가 아님({markers.get('AWS_ENABLED')})")
        need(claude, CLAUDE, [("AWS·EC2 추가 금지 규칙", r"AWS·EC2")])
        need(skill, SKILL, [("AWS·EC2 금지", r"AWS·EC2")])

    @check(13, "EXCLUDED 보호 규칙 존재")
    def _():
        need(claude, CLAUDE, EXCLUDED_IDS + [("EXCLUDED 임의 구현 금지", r"EXCLUDED 기능.*임의로 구현하지 않는다")])
        need(skill, SKILL, ["EXCLUDED 보호"] + EXCLUDED_IDS)

    failed = 0
    for num, title, fn in checks:
        before = len(errors)
        fn()
        ok = len(errors) == before
        failed += (not ok)
        print(f"[{'OK' if ok else 'FAIL'}] {num:>2}. {title}")
    for e in errors:
        print(f"ERROR {e}")
    if errors:
        print(f"VALIDATE_HARNESS_FAIL ({len(errors)} errors, {failed}/{len(checks)} checks failed)")
        return 1
    print(f"VALIDATE_HARNESS_PASS checks={len(checks)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
