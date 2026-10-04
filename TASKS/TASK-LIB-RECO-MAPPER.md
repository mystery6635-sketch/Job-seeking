# TASK-LIB-RECO-MAPPER 감점 항목 기반 추천 매핑

- Task ID: LIB-RECO-MAPPER
- Seq: 15
- Category: LOGIC
- Priority: P0
- Status: NOT_STARTED

## Context

감점 항목 기반 추천 매핑. UI와 무관한 순수 함수를 만들어 단위 테스트로 검증 가능하게 한다.

선행 Task: `DATA-RECOMMENDATIONS`, `LIB-DEDUCTION-REASONS`.

이 Task에 의존하는 Task: `DB-ACCESS`, `API-DIAG-SUBMIT`, `UNIT-REASONS-RECO`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-RECO-001: `src/data` 하드코딩 정적 매핑 테이블로 감점 항목 기반 추천 리스트 제공, 감점 항목 없으면 대체 안내

## Requirement Ref

- REQ-FUNC-RECO-001 (IMPLEMENT) — SRS §4.3.3 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: SCR-003
- Route: —
- Page Entry: —

## Design Ref

- `docs/06_SRS_UIUX_REVISED.md` §4.3.3 — 시각 규칙 없음

## Depends On

- `DATA-RECOMMENDATIONS` — 자격증·훈련 추천 정적 데이터
- `LIB-DEDUCTION-REASONS` — 감점 근거 도출

## Expected Files

- create: src/lib/diagnosis/recommend.ts
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. `mapRecommendations(deductions)`는 `감점 있음` 카테고리에 대응하는 `DATA-RECOMMENDATIONS` 항목을 정적 매핑 순서대로 반환한다(개인화·점수 가중 정렬 없음)
2. 감점 항목이 없으면 `{ empty: true }`를 반환해 UI가 `보완이 필요한 항목이 없습니다` Empty State를 쓰게 한다
3. `priority_order`는 사용하지 않는다

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. 해당 없음

## Test Cases

- REQ-FUNC-RECO-001: TC-RECO-001-DRAFT

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
