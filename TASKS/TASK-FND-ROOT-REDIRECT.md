# TASK-FND-ROOT-REDIRECT 루트 Starter 제거와 /diagnosis redirect

- Task ID: FND-ROOT-REDIRECT
- Seq: 3
- Category: FOUNDATION
- Priority: P0
- Status: NOT_STARTED

## Context

루트 Starter 제거와 /diagnosis redirect. 여러 Screen이 공유하는 기반을 만든다.

선행 Task: `FND-TOKENS`.

이 Task에 의존하는 Task: `PAGE-SCR001`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- 이 Task는 특정 Requirement에 직접 대응하지 않는 지원 Task이며, 연결된 Task를 가능하게 하는 범위로 한정한다.

## Requirement Ref

- 없음 (지원 Task)

## Screen / Route / Page Entry

- Screen: 기술 Route(Screen 아님)
- Route: `/`
- Page Entry: `src/app/page.tsx`

## Design Ref

- `design-reference/UI_CONTRACT.md` §0 공통 계약(`/`는 Screen이 아닌 기술 Route)
- `design-reference/SCREEN_ROUTE_CONTRACT.json` technical_routes(`/`)

## Depends On

- `FND-TOKENS` — D-001 Token CSS와 루트 레이아웃

## Expected Files

- modify: src/app/page.tsx
- delete: public/next.svg
- delete: public/vercel.svg
- delete: public/file.svg
- delete: public/globe.svg
- delete: public/window.svg
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. Next.js 구현 전 `node_modules/next/dist/docs/` 관련 문서 확인(AGENTS.md)
2. `src/app/page.tsx`는 `/diagnosis`로 redirect하며 create-next-app Starter 화면·문구(`To get started`, `next.svg`)를 남기지 않는다
3. 참조되지 않는 Starter 정적 자산을 삭제한다

## Visual AC

1. `/` 접근 시 Starter 화면이 한 프레임도 보이지 않는다

## Security/Privacy AC

1. redirect 대상은 내부 경로 `/diagnosis`로 고정한다(open redirect 금지)

## Test Cases

- 대응하는 SRS Test Case 없음 — 검증은 Verify의 명령·확인 항목으로 한다

## Verify

- `npm run build`, 브라우저에서 `/` 접근 시 `/diagnosis`로 이동

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목을 모두 충족했다
- [ ] Verify의 명령·확인을 실행해 결과를 기록했다(통과하지 못하면 완료로 보고하지 않는다)
- [ ] Expected Files에 없는 파일을 수정하지 않았다
- [ ] Forbidden 항목에 해당하는 변경이 없다
- [ ] `npm run lint`·`npm run build`가 통과한다

## Forbidden

- Expected Files 밖 파일 수정·생성 금지(필요하면 먼저 `TASKS/00_TASK_LIST.md`를 고친다)
- 로그인·계정·관리자·결제·별점·광고 UI·Route 추가 금지
- D-001 Token에 없는 색·간격·그림자 추가 금지
- `Lorem ipsum`·`준비 중`·`정보 확인 필요`·`TBD` 등 Placeholder 문구 금지
- 자동 Merge·EC2·AWS 설정 추가 금지
- 구현 코드·Branch·Commit을 이 문서 작업으로 만들지 않는다
