# TASK-LIB-SCORING-ENGINE 100점 진단 점수 산출 엔진

- Task ID: LIB-SCORING-ENGINE
- Seq: 13
- Category: LOGIC
- Priority: P0
- Status: NOT_STARTED

## Context

100점 진단 점수 산출 엔진. UI와 무관한 순수 함수를 만들어 단위 테스트로 검증 가능하게 한다.

선행 Task: `LIB-INPUT-VALIDATION`.

이 Task에 의존하는 Task: `LIB-DEDUCTION-REASONS`, `API-DIAG-SUBMIT`, `UNIT-SCORING`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-DIAG-001: 학력·나이·경력·자격증·skill 입력을 받아 100점 만점 점수를 산출하는 결정적 채점 함수 구현
- REQ-FUNC-DIAG-003: 채점 로직을 순수 함수로 구현하여 동일 입력에 동일 점수를 보장
- REQ-NFR-PERF-001: 진단 요청 후 5초 이내 결과 반환을 목표로 채점 로직을 동기·경량 함수로 구현

## Requirement Ref

- REQ-FUNC-DIAG-001 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-DIAG-003 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-NFR-PERF-001 (IMPLEMENT) — SRS §4.4.1 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: SCR-001, SCR-002
- Route: —
- Page Entry: —

## Design Ref

- `docs/06_SRS_UIUX_REVISED.md` §4.3.1, §4.3.1, §4.4.1 — 시각 규칙 없음

## Depends On

- `LIB-INPUT-VALIDATION` — 진단 입력 검증

## Expected Files

- create: src/lib/diagnosis/scoring.ts
- create: src/data/scoring-rules.ts
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. `computeScore(input)`은 시간·난수·외부 호출 없는 순수 함수이며 동일 입력에 항상 동일한 0~100 정수 점수와 카테고리별 점수를 반환한다
2. 4개 카테고리(학력·경력·자격증·스킬)를 균등 25점 만점으로 계산하고 총점은 합(0~100)이다. 구간표 값은 `docs/PROJECT_SCOPE.md` §6.1(OQ-08 확정)을 `src/data/scoring-rules.ts` 한 곳에 그대로 옮긴다. 나이는 점수에 반영하지 않는다
3. 동기·경량 함수로 구현해 5초 목표를 위협하지 않는다

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. 점수 계산 중 입력 원문을 로그로 남기지 않는다

## Test Cases

- REQ-FUNC-DIAG-001: TC-DIAG-001-N
- REQ-FUNC-DIAG-003: TC-DIAG-003-N
- REQ-NFR-PERF-001: TC-NFR-PERF-001

## Verify

- `UNIT-SCORING`

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목을 모두 충족했다
- [ ] Verify의 명령·확인을 실행해 결과를 기록했다(통과하지 못하면 완료로 보고하지 않는다)
- [ ] Expected Files에 없는 파일을 수정하지 않았다
- [ ] Forbidden 항목에 해당하는 변경이 없다
- [ ] 대응 단위 테스트가 통과한다

## Forbidden

- Expected Files 밖 파일 수정·생성 금지(필요하면 먼저 `TASKS/00_TASK_LIST.md`를 고친다)
- 로그인·계정·관리자·결제·별점·광고 UI·Route 추가 금지
- D-001 Token에 없는 색·간격·그림자 추가 금지
- `Lorem ipsum`·`준비 중`·`정보 확인 필요`·`TBD` 등 Placeholder 문구 금지
- 자동 Merge·EC2·AWS 설정 추가 금지
- 구현 코드·Branch·Commit을 이 문서 작업으로 만들지 않는다
- MBTI 지표를 핵심 100점과 합산하는 코드 금지
- 시간·난수·외부 호출에 의존하는 점수 계산 금지
