# TASK-UNIT-SCORING 점수 산출 단위 테스트

- Task ID: UNIT-SCORING
- Seq: 41
- Category: TEST
- Priority: P0
- Status: NOT_STARTED

## Context

점수 산출 단위 테스트. 구현이 Requirement와 AC를 만족하는지 자동 테스트로 확인한다.

선행 Task: `LIB-SCORING-ENGINE`, `FND-TEST-TOOLING`.

이 Task에 의존하는 Task: `OPS-CI`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-DIAG-001: 학력·나이·경력·자격증·skill 입력을 받아 100점 만점 점수를 산출하는 결정적 채점 함수 구현
- REQ-FUNC-DIAG-003: 채점 로직을 순수 함수로 구현하여 동일 입력에 동일 점수를 보장

## Requirement Ref

- REQ-FUNC-DIAG-001 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-DIAG-003 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: —
- Route: —
- Page Entry: —

## Design Ref

- `docs/06_SRS_UIUX_REVISED.md` §4.3.1, §4.3.1 — 시각 규칙 없음

## Depends On

- `LIB-SCORING-ENGINE` — 100점 진단 점수 산출 엔진
- `FND-TEST-TOOLING` — 테스트 도구 설정(Vitest, Playwright Chromium)

## Expected Files

- create: tests/unit/scoring.test.ts
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. 입력 세트별 점수가 0~100 정수이고 동일 입력 100회 호출 결과가 항상 같다(TC-DIAG-001-N, TC-DIAG-003-N)
2. 자격증·skill `없음` 입력과 PROJECT_SCOPE §6.1 구간 경계값(경력 1·3·5·10년, 자격증 1~4개, 스킬 1·3·5·7개)별 점수·총점 합 25×4를 검증한다

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. 테스트 데이터에 실제 개인정보를 쓰지 않는다

## Test Cases

- REQ-FUNC-DIAG-001: TC-DIAG-001-N
- REQ-FUNC-DIAG-003: TC-DIAG-003-N
- 이 Task가 수행하는 케이스: Functional AC 각 항목

## Verify

- `npm run test -- scoring`

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
