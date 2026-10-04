# TASK-FND-TEST-TOOLING 테스트 도구 설정(Vitest, Playwright Chromium)

- Task ID: FND-TEST-TOOLING
- Seq: 1
- Category: FOUNDATION
- Priority: P0
- Status: NOT_STARTED

## Context

테스트 도구 설정(Vitest, Playwright Chromium). 여러 Screen이 공유하는 기반을 만든다.

선행 Task: 없음.

이 Task에 의존하는 Task: `FND-TOKENS`, `UNIT-SCORING`, `UNIT-VALIDATION`, `UNIT-REASONS-RECO`, `UNIT-JOBLINK`, `UNIT-MBTI-MAP`, `E2E-PUBLIC-SMOKE`, `E2E-DIAG-FLOW`, `E2E-JOBS-ATTITUDE`, `OPS-CI`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- 이 Task는 특정 Requirement에 직접 대응하지 않는 지원 Task이며, 연결된 Task를 가능하게 하는 범위로 한정한다.

## Requirement Ref

- 없음 (지원 Task)

## Screen / Route / Page Entry

- Screen: —
- Route: —
- Page Entry: —

## Design Ref

- 해당 없음 — 시각 규칙이 없는 Task다. 화면에 영향이 생기면 D-001 Token만 사용한다.

## Depends On

- 없음

## Expected Files

- modify: package.json
- create: vitest.config.ts
- create: playwright.config.ts
- create: tests/.gitkeep
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. `npm run test`(Vitest)와 `npm run e2e`(Playwright)가 동작한다
2. Playwright project는 `chromium` 하나만 정의한다(Firefox·WebKit·부하 테스트 금지)
3. Playwright `webServer`는 `npm run dev`를 사용한다

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. 테스트 설정에 실제 개인정보·키를 넣지 않는다

## Test Cases

- 대응하는 SRS Test Case 없음 — 검증은 Verify의 명령·확인 항목으로 한다

## Verify

- `npm run test -- --run`, `npx playwright test --list`

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
