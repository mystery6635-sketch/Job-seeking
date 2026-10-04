# TASK-UNIT-VALIDATION 입력 검증 단위 테스트

- Task ID: UNIT-VALIDATION
- Seq: 42
- Category: TEST
- Priority: P0
- Status: NOT_STARTED

## Context

입력 검증 단위 테스트. 구현이 Requirement와 AC를 만족하는지 자동 테스트로 확인한다.

선행 Task: `LIB-INPUT-VALIDATION`, `FND-TEST-TOOLING`.

이 Task에 의존하는 Task: `OPS-CI`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-DIAG-002: 필수 항목(학력·나이·경력) 누락 시 점수 산출 이전에 검증하여 누락 항목을 명시한 오류 메시지 표시
- REQ-NFR-PRIV-001: 입력 폼을 진단에 필요한 항목(학력·나이·경력·자격증·skill)과 희망 직무로만 한정 설계

## Requirement Ref

- REQ-FUNC-DIAG-002 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-NFR-PRIV-001 (IMPLEMENT) — SRS §4.4.3 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: —
- Route: —
- Page Entry: —

## Design Ref

- `docs/06_SRS_UIUX_REVISED.md` §4.3.1, §4.4.3 — 시각 규칙 없음

## Depends On

- `LIB-INPUT-VALIDATION` — 진단 입력 검증
- `FND-TEST-TOOLING` — 테스트 도구 설정(Vitest, Playwright Chromium)

## Expected Files

- create: tests/unit/validate.test.ts
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. 학력·나이·경력 각각 누락 및 전체 누락에서 누락 필드 목록을 반환하고 점수는 계산하지 않는다(TC-DIAG-002-F)
2. 입력 타입에 정의 외 개인정보 필드가 없음을 검증한다

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. 정의되지 않은 필드는 무시됨을 테스트한다

## Test Cases

- REQ-FUNC-DIAG-002: TC-DIAG-002-F
- REQ-NFR-PRIV-001: TC-NFR-PRIV-001
- 이 Task가 수행하는 케이스: Functional AC 각 항목

## Verify

- `npm run test -- validate`

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목을 모두 충족했다
- [ ] Verify의 명령·확인을 실행해 결과를 기록했다(통과하지 못하면 완료로 보고하지 않는다)
- [ ] Expected Files에 없는 파일을 수정하지 않았다
- [ ] Forbidden 항목에 해당하는 변경이 없다
- [ ] 테스트가 현재 구현에서 통과한다

## Forbidden

- Expected Files 밖 파일 수정·생성 금지(필요하면 먼저 `TASKS/00_TASK_LIST.md`를 고친다)
- 로그인·계정·관리자·결제·별점·광고 UI·Route 추가 금지
- D-001 Token에 없는 색·간격·그림자 추가 금지
- `Lorem ipsum`·`준비 중`·`정보 확인 필요`·`TBD` 등 Placeholder 문구 금지
- 자동 Merge·EC2·AWS 설정 추가 금지
- 구현 코드·Branch·Commit을 이 문서 작업으로 만들지 않는다
- 운영 DB 키·실제 개인정보 사용 금지
