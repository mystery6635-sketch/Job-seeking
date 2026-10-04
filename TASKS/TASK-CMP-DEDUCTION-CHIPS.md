# TASK-CMP-DEDUCTION-CHIPS 카테고리 Chip 목록

- Task ID: CMP-DEDUCTION-CHIPS
- Seq: 31
- Category: COMPONENT
- Priority: P0
- Status: NOT_STARTED

## Context

카테고리 Chip 목록. 화면에 쓰이는 컴포넌트를 만든다. Page Entry는 만들지 않는다.

선행 Task: `FND-TOKENS`.

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

- `design-reference/D-001/DESIGN.md` §11 Result Item Card, §18 Section별 위계
- `design-reference/UI_CONTRACT.md` SCR-002 영역 순서 4

## Depends On

- `FND-TOKENS` — D-001 Token CSS와 루트 레이아웃

## Expected Files

- create: src/components/result/DeductionChipList.tsx
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. Next.js 구현 전 `node_modules/next/dist/docs/` 관련 문서 확인(AGENTS.md)
2. 학력·경력·자격증·스킬 4개 카테고리를 Chip으로 보여주고 각 Chip 옆에 감점 사유 한 문장(또는 `감점 없음`)을 표시한다

## Visual AC

1. Chip 색은 상태(감점 있음/없음)를 아이콘·텍스트와 함께 구분하며 색만으로 구분하지 않는다

## Security/Privacy AC

1. 해당 없음

## Test Cases

- REQ-FUNC-SCORE-001: TC-SCORE-001-N
- REQ-FUNC-SCORE-002: TC-SCORE-002-N

## Verify

- `npm run lint`, `npm run build`

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
