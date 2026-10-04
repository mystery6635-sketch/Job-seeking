# TASK-CMP-REASON-DRAWER 감점 근거 Drawer

- Task ID: CMP-REASON-DRAWER
- Seq: 30
- Category: COMPONENT
- Priority: P0
- Status: NOT_STARTED

## Context

감점 근거 Drawer. 화면에 쓰이는 컴포넌트를 만든다. Page Entry는 만들지 않는다.

선행 Task: `FND-FEEDBACK`, `API-DIAG-REASONS`, `FEAT-OBS-EVENTS`.

이 Task에 의존하는 Task: `PAGE-SCR002`.

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

- `design-reference/D-001/DESIGN.md` §12 Drawer · Modal, §14 Loading · Error, §15
- `design-reference/UI_CONTRACT.md` SCR-002 상태·이동

## Depends On

- `FND-FEEDBACK` — 공통 Alert·Toast·EmptyState·Skeleton
- `API-DIAG-REASONS` — GET /api/diagnosis/[result_id]/reasons (API-03)
- `FEAT-OBS-EVENTS` — KPI 이벤트 기록(진단 완료·근거 화면 도달)

## Expected Files

- create: src/components/result/ReasonDrawer.tsx
- create: src/components/result/ReasonItemCard.tsx
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. Next.js 구현 전 `node_modules/next/dist/docs/` 관련 문서 확인(AGENTS.md)
2. 별도 Route 없이 같은 화면의 Drawer로 열고 Esc·Scrim 클릭으로 닫는다. Drawer가 열리면 포커스를 가두고 닫으면 트리거로 되돌린다
3. 항목 4개를 표시하고 `감점 없음` 항목은 구분 표시한다. Drawer 열림 시 `reasons_viewed` 이벤트를 1회 기록한다

## Visual AC

1. Desktop 우측 480px 패널, Mobile 하단 시트(최대 90vh)
2. 로딩은 Skeleton, 실패는 `error` Alert+`다시 시도`

## Security/Privacy AC

1. `/diagnosis/result/reasons` Route를 만들지 않는다

## Test Cases

- REQ-FUNC-SCORE-001: TC-SCORE-001-N
- REQ-FUNC-SCORE-002: TC-SCORE-002-N

## Verify

- `npm run lint`, `npm run build`, 키보드 Esc·Tab 포커스 트랩 확인

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
