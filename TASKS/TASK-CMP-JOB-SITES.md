# TASK-CMP-JOB-SITES 구인 사이트 연결 Card Grid

- Task ID: CMP-JOB-SITES
- Seq: 33
- Category: COMPONENT
- Priority: P1
- Status: NOT_STARTED

## Context

구인 사이트 연결 Card Grid. 화면에 쓰이는 컴포넌트를 만든다. Page Entry는 만들지 않는다.

선행 Task: `FND-FEEDBACK`, `LIB-JOBLINK-BUILDER`, `API-DIAG-JOBS`.

이 Task에 의존하는 Task: `PAGE-SCR004`, `MANUAL-JOBLINKS`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-JOBLINK-001: 희망 직무 문자열을 사이트별 검색 URL 템플릿에 치환해 잡코리아·사람인·원티드·워크넷·IT 전문 구인 사이트 링크를 새 탭으로 연결(매칭·추천 로직 없음)
- REQ-FUNC-JOBLINK-002: 희망 직무 정보 없음 시 안내 문구와 재진단 CTA 표시

## Requirement Ref

- REQ-FUNC-JOBLINK-001 (IMPLEMENT) — SRS §4.3.3b (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-JOBLINK-002 (IMPLEMENT) — SRS §4.3.3b (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: SCR-004
- Route: —
- Page Entry: —

## Design Ref

- `design-reference/D-001/DESIGN.md` §8 Search · Filter, §9 Card, §14 Empty(SCR-004), §21 Do
- `design-reference/UI_CONTRACT.md` SCR-004

## Depends On

- `FND-FEEDBACK` — 공통 Alert·Toast·EmptyState·Skeleton
- `LIB-JOBLINK-BUILDER` — 희망 직무 → 검색 링크 생성
- `API-DIAG-JOBS` — GET /api/diagnosis/[result_id]/jobs (API-06)

## Expected Files

- create: src/components/jobs/JobQueryBar.tsx
- create: src/components/jobs/JobSiteCard.tsx
- create: src/components/jobs/JobSiteGrid.tsx
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. Next.js 구현 전 `node_modules/next/dist/docs/` 관련 문서 확인(AGENTS.md)
2. 희망 직무가 있으면 사이트 Card 6개 이상과 JobQueryBar(희망 직무 표시)를, 없으면 EmptyState(`희망 직무를 입력하면 채용 사이트를 바로 연결해 드립니다`, CTA `진단 입력하기`)를 보여주며 둘은 동시에 보이지 않는다
3. 각 Card의 `희망 직무로 검색하기`는 새 탭(`target="_blank"`)으로 열리고 `rel="noopener noreferrer"`와 외부 이동 아이콘을 가진다
4. `특정 공고를 선별·추천하지 않으며 희망 직무는 검색창 채움 용도로만 사용됩니다` 고지를 Grid 하단에 표시한다

## Visual AC

1. Desktop 3열·Mobile 1열, 고지 문장이 Grid 하단에 보인다

## Security/Privacy AC

1. 외부 링크 `rel` 누락 금지, 공고 feed·랭킹·로고 이미지 금지

## Test Cases

- REQ-FUNC-JOBLINK-001: TC-JOBLINK-001-N
- REQ-FUNC-JOBLINK-002: TC-JOBLINK-002-F

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
