# TASK-DATA-RECOMMENDATIONS 자격증·훈련 추천 정적 데이터

- Task ID: DATA-RECOMMENDATIONS
- Seq: 9
- Category: DATA
- Priority: P0
- Status: NOT_STARTED

## Context

자격증·훈련 추천 정적 데이터. `src/data`의 하드코딩 정적 데이터를 만든다(외부 연동·DB 저장 없음).

선행 Task: 없음.

이 Task에 의존하는 Task: `LIB-RECO-MAPPER`, `PAGE-SCR003`, `UNIT-REASONS-RECO`.

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

- `design-reference/D-001/DESIGN.md` §9 Recommendation Card, §20 Placeholder 금지
- `design-reference/UI_CONTRACT.md` SCR-003

## Depends On

- 없음

## Expected Files

- create: src/data/recommendations.ts
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. 감점 카테고리 4개(학력·경력·자격증·스킬)마다 추천 항목 2개 이상, 전체 8개 이상을 `src/data` 하드코딩 테이블로 둔다(외부 데이터 연동·DB 저장 없음)
2. 각 항목은 `title`, `category`, `summary`(1~2문장), `how_to`를 가지며 실제 자격증·훈련 과정명을 쓴다

## Visual AC

1. `Lorem ipsum`·`준비 중`·빈 항목이 없고 모든 항목이 한국어 실제 콘텐츠다

## Security/Privacy AC

1. 가격·별점·후기·신청 링크·광고 필드를 두지 않는다

## Test Cases

- REQ-FUNC-RECO-001: TC-RECO-001-DRAFT

## Verify

- `UNIT-REASONS-RECO`, 타입 검사

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목을 모두 충족했다
- [ ] Verify의 명령·확인을 실행해 결과를 기록했다(통과하지 못하면 완료로 보고하지 않는다)
- [ ] Expected Files에 없는 파일을 수정하지 않았다
- [ ] Forbidden 항목에 해당하는 변경이 없다
- [ ] 대응 단위 테스트가 통과하고 빈 필드가 없다

## Forbidden

- Expected Files 밖 파일 수정·생성 금지(필요하면 먼저 `TASKS/00_TASK_LIST.md`를 고친다)
- 로그인·계정·관리자·결제·별점·광고 UI·Route 추가 금지
- D-001 Token에 없는 색·간격·그림자 추가 금지
- `Lorem ipsum`·`준비 중`·`정보 확인 필요`·`TBD` 등 Placeholder 문구 금지
- 자동 Merge·EC2·AWS 설정 추가 금지
- 구현 코드·Branch·Commit을 이 문서 작업으로 만들지 않는다
- 외부 데이터 연동·크롤링·공고 매칭·추천 로직 금지
