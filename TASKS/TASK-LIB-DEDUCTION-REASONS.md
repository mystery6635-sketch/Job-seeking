# TASK-LIB-DEDUCTION-REASONS 감점 근거 도출

- Task ID: LIB-DEDUCTION-REASONS
- Seq: 14
- Category: LOGIC
- Priority: P0
- Status: NOT_STARTED

## Context

감점 근거 도출. UI와 무관한 순수 함수를 만들어 단위 테스트로 검증 가능하게 한다.

선행 Task: `LIB-SCORING-ENGINE`.

이 Task에 의존하는 Task: `LIB-RECO-MAPPER`, `DB-ACCESS`, `API-DIAG-SUBMIT`, `UNIT-REASONS-RECO`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-SCORE-001: 진단 완료 후 "근거 보기" 클릭 시 항목별 감점 사유를 최소 3개 이상 표시
- REQ-FUNC-SCORE-002: 만점 항목은 "감점 없음"으로 구분 표시

## Requirement Ref

- REQ-FUNC-SCORE-001 (IMPLEMENT) — SRS §4.3.2 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-SCORE-002 (IMPLEMENT) — SRS §4.3.2 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: SCR-002
- Route: —
- Page Entry: —

## Design Ref

- `docs/06_SRS_UIUX_REVISED.md` §4.3.2, §4.3.2 — 시각 규칙 없음

## Depends On

- `LIB-SCORING-ENGINE` — 100점 진단 점수 산출 엔진

## Expected Files

- create: src/lib/diagnosis/deductions.ts
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. `buildDeductionItems(score)`는 학력·경력·자격증·스킬 4개 카테고리 항목을 항상 반환하고 각 항목은 `status`(`감점 있음`/`감점 없음`)와 감점 있음일 때 비어 있지 않은 `reason_text`를 가진다
2. 만점 카테고리는 `감점 없음`으로 구분한다(감점 근거 최소 3개 항목 표시 요건 충족)
3. 사유 도출 규칙은 OQ-13 결정을 따르며 룰 테이블(`scoring-rules.ts`)에서만 읽는다

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. `reason_text`에 입력 원문 전체를 복사하지 않고 카테고리·기준 중심 문장으로 작성한다

## Test Cases

- REQ-FUNC-SCORE-001: TC-SCORE-001-N
- REQ-FUNC-SCORE-002: TC-SCORE-002-N

## Verify

- `UNIT-REASONS-RECO`

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
