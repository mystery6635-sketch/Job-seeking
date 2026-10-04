# TASK-MANUAL-LOGS-OBS 저장 암호화·접근 로그·KPI 이벤트 확인

- Task ID: MANUAL-LOGS-OBS
- Seq: 53
- Category: MANUAL
- Priority: P1
- Status: NOT_STARTED

## Context

저장 암호화·접근 로그·KPI 이벤트 확인. 자동화하지 않는 항목을 수동으로 확인하고 증거를 남긴다.

선행 Task: `DB-SCHEMA-BASE`, `FEAT-OBS-EVENTS`, `OPS-VERCEL-DB-CHECK`.

이 Task에 의존하는 Task: `RELEASE-CHECK`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-NFR-SEC-001: 관리형 DB의 기본 저장 암호화 기능 활용, 커스텀 암호화 계층은 만들지 않음
- REQ-NFR-SEC-003: 커스텀 감사 로그 대신 호스팅/DB 플랫폼 기본 접근 로그 활용(Dummy)
- REQ-NFR-OBS-001: 무료 분석 도구로 진단 완료·근거 화면 도달 이벤트만 최소 기록(Dummy)

## Requirement Ref

- REQ-NFR-SEC-001 (IMPLEMENT) — SRS §4.4.3 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-NFR-SEC-003 (IMPLEMENT) — SRS §4.4.3 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-NFR-OBS-001 (IMPLEMENT) — SRS §4.4.4 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: —
- Route: —
- Page Entry: —

## Design Ref

- `docs/06_SRS_UIUX_REVISED.md` §4.4.4, §4.4.3, §4.4.3 — 시각 규칙 없음

## Depends On

- `DB-SCHEMA-BASE` — DB 스키마(4개 테이블)
- `FEAT-OBS-EVENTS` — KPI 이벤트 기록(진단 완료·근거 화면 도달)
- `OPS-VERCEL-DB-CHECK` — Vercel 수동 배포와 DB 연결·플랫폼 로그 설정

## Expected Files

- create: TASKS/evidence/ops-check.md
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. 관리형 DB 기본 저장 암호화 활성 설정, 호스팅/DB 플랫폼 접근 로그 존재, 분석 도구에서 `diagnosis_completed`·`reasons_viewed` 수신을 각각 확인해 기록한다

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. 확인 기록에 키·개인정보 값을 남기지 않는다

## Test Cases

- REQ-NFR-SEC-001: TC-NFR-SEC-001
- REQ-NFR-SEC-003: TC-NFR-SEC-003
- REQ-NFR-OBS-001: TC-NFR-OBS-001-DRAFT
- 이 Task가 수행하는 케이스: Functional AC 각 항목

## Verify

- 수동 확인

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목을 모두 충족했다
- [ ] Verify의 명령·확인을 실행해 결과를 기록했다(통과하지 못하면 완료로 보고하지 않는다)
- [ ] Expected Files에 없는 파일을 수정하지 않았다
- [ ] Forbidden 항목에 해당하는 변경이 없다
- [ ] `TASKS/evidence/`에 확인 결과를 기록했다

## Forbidden

- Expected Files 밖 파일 수정·생성 금지(필요하면 먼저 `TASKS/00_TASK_LIST.md`를 고친다)
- 로그인·계정·관리자·결제·별점·광고 UI·Route 추가 금지
- D-001 Token에 없는 색·간격·그림자 추가 금지
- `Lorem ipsum`·`준비 중`·`정보 확인 필요`·`TBD` 등 Placeholder 문구 금지
- 자동 Merge·EC2·AWS 설정 추가 금지
- 구현 코드·Branch·Commit을 이 문서 작업으로 만들지 않는다
