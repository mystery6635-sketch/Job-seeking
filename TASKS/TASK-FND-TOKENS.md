# TASK-FND-TOKENS D-001 Token CSS와 루트 레이아웃

- Task ID: FND-TOKENS
- Seq: 2
- Category: FOUNDATION
- Priority: P0
- Status: NOT_STARTED

## Context

D-001 Token CSS와 루트 레이아웃. 여러 Screen이 공유하는 기반을 만든다.

선행 Task: `FND-TEST-TOOLING`.

이 Task에 의존하는 Task: `FND-ROOT-REDIRECT`, `FND-NOT-FOUND`, `FND-SHELL`, `FND-FEEDBACK`, `FND-SECTIONS`, `CMP-FIELDS`, `CMP-DEDUCTION-CHIPS`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- 이 Task는 특정 Requirement에 직접 대응하지 않는 지원 Task이며, 연결된 Task를 가능하게 하는 범위로 한정한다.

## Requirement Ref

- 없음 (지원 Task)

## Screen / Route / Page Entry

- Screen: 전체
- Route: —
- Page Entry: —

## Design Ref

- `design-reference/D-001/DESIGN.md` §1 Visual Theme, §2 Color Token, §3 Typography, §4 Spacing, §5 Radius, §6 Shadow, §16 Page Section 최대 폭, §21 Do / Do Not

## Depends On

- `FND-TEST-TOOLING` — 테스트 도구 설정(Vitest, Playwright Chromium)

## Expected Files

- modify: src/app/globals.css
- modify: src/app/layout.tsx
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. Next.js 구현 전 `node_modules/next/dist/docs/` 관련 문서 확인(AGENTS.md)
2. `globals.css`에 D-001 §2~6 Token(색·타이포·간격·반경·그림자)만 CSS 변수로 정의한다
3. `layout.tsx`는 `lang="ko"`, 서비스 `metadata`(title·description), SiteHeader·SiteFooter 슬롯을 가진다
4. Inter는 Google Fonts 링크로만 로드하고 폰트 파일을 저장소에 넣지 않는다

## Visual AC

1. D-001에 없는 색·그라디언트·그림자를 추가하지 않는다
2. accent(파랑)는 오류·경고·안내 용도로 쓰지 않는다
3. Section 최대 폭 1200px, 상하 여백 Desktop 80px·Mobile 48px을 유틸 클래스로 제공한다

## Security/Privacy AC

1. Token CSS에 계정·결제·광고 관련 구성을 만들지 않는다

## Test Cases

- 대응하는 SRS Test Case 없음 — 검증은 Verify의 명령·확인 항목으로 한다

## Verify

- `npm run lint`, `npm run build`

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
