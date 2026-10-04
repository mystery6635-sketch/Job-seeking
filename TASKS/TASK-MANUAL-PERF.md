# TASK-MANUAL-PERF 응답 시간 수동 측정

- Task ID: MANUAL-PERF
- Seq: 50
- Category: MANUAL
- Priority: P0
- Status: NOT_STARTED

## Context

응답 시간 수동 측정. 자동화하지 않는 항목을 수동으로 확인하고 증거를 남긴다.

선행 Task: `API-DIAG-SUBMIT`, `CMP-DIAG-FORM`.

이 Task에 의존하는 Task: `RELEASE-CHECK`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-NFR-PERF-001: 진단 요청 후 5초 이내 결과 반환을 목표로 채점 로직을 동기·경량 함수로 구현

## Requirement Ref

- REQ-NFR-PERF-001 (IMPLEMENT) — SRS §4.4.1 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: —
- Route: —
- Page Entry: —

## Design Ref

- `docs/06_SRS_UIUX_REVISED.md` §4.4.1 — 시각 규칙 없음

## Depends On

- `API-DIAG-SUBMIT` — POST /api/diagnosis (API-01)
- `CMP-DIAG-FORM` — 진단 입력 Form 컴포넌트

## Expected Files

- create: TASKS/evidence/perf-check.md
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. 개발자 도구 Network에서 진단 제출 응답 시간을 5회 측정해 모두 5초 이내임을 기록한다

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. 측정 입력은 가상 데이터

## Test Cases

- REQ-NFR-PERF-001: TC-NFR-PERF-001
- 이 Task가 수행하는 케이스: Functional AC 각 항목

## Verify

- 수동 측정 기록

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
