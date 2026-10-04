# TASK-CMP-RECO-GRID 추천 Card Grid

- Task ID: CMP-RECO-GRID
- Seq: 32
- Category: COMPONENT
- Priority: P0
- Status: NOT_STARTED

## Context

추천 Card Grid. 화면에 쓰이는 컴포넌트를 만든다. Page Entry는 만들지 않는다.

선행 Task: `FND-FEEDBACK`, `API-DIAG-RECOMMENDATIONS`.

이 Task에 의존하는 Task: `PAGE-SCR003`.

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

- `design-reference/D-001/DESIGN.md` §9 Recommendation Card, §14 Empty(SCR-003), §15 Card Grid
- `design-reference/UI_CONTRACT.md` SCR-003

## Depends On

- `FND-FEEDBACK` — 공통 Alert·Toast·EmptyState·Skeleton
- `API-DIAG-RECOMMENDATIONS` — GET /api/diagnosis/[result_id]/recommendations (API-04)

## Expected Files

- create: src/components/recommend/RecommendationCard.tsx
- create: src/components/recommend/RecommendationGrid.tsx
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. Next.js 구현 전 `node_modules/next/dist/docs/` 관련 문서 확인(AGENTS.md)
2. 추천 목록이 6개 이상이면 Grid를, 감점 없음(`empty`)이면 EmptyState(`보완이 필요한 항목이 없습니다`, CTA `결과로 돌아가기`)를 렌더링하며 둘은 동시에 보이지 않는다
3. 6개 미만이면 Grid를 렌더링하지 않고 완성형 Empty State로 대체한다

## Visual AC

1. Desktop 3열(간격 20px)·Mobile 1열, Card마다 제목·카테고리·설명이 모두 채워져 있다

## Security/Privacy AC

1. 과정 신청·결제·가격·별점·광고 Card를 만들지 않는다

## Test Cases

- REQ-FUNC-RECO-001: TC-RECO-001-DRAFT

## Verify

- `npm run lint`, `npm run build`, `E2E-JOBS-ATTITUDE`

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목을 모두 충족했다
- [ ] Verify의 명령·확인을 실행해 결과를 기록했다(통과하지 못하면 완료로 보고하지 않는다)
- [ ] Expected Files에 없는 파일을 수정하지 않았다
- [ ] Forbidden 항목에 해당하는 변경이 없다
- [ ] 구현 전 `node_modules/next/dist/docs/` 관련 문서를 확인했다
- [ ] `npm run lint`·`npm run build`가 통과한다

## Forbidden

- Expected Files 밖 파일 수정·생성 금지(필요하면 먼저 `TASKS/00_TASK_LIST.md`를 고친다)
- 로그인·계정·관리자·결제·별점·광고 UI·Route 추가 금지
- D-001 Token에 없는 색·간격·그림자 추가 금지
- `Lorem ipsum`·`준비 중`·`정보 확인 필요`·`TBD` 등 Placeholder 문구 금지
- 자동 Merge·EC2·AWS 설정 추가 금지
- 구현 코드·Branch·Commit을 이 문서 작업으로 만들지 않는다
- Page Entry(`page.tsx`)를 만들거나 수정하지 않는다
