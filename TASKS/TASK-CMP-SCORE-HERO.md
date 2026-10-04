# TASK-CMP-SCORE-HERO 결과 Hero·게이지·입력값 요약

- Task ID: CMP-SCORE-HERO
- Seq: 29
- Category: COMPONENT
- Priority: P0
- Status: NOT_STARTED

## Context

결과 Hero·게이지·입력값 요약. 화면에 쓰이는 컴포넌트를 만든다. Page Entry는 만들지 않는다.

선행 Task: `FND-SECTIONS`.

이 Task에 의존하는 Task: `PAGE-SCR002`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-DIAG-001: 학력·나이·경력·자격증·skill 입력을 받아 100점 만점 점수를 산출하는 결정적 채점 함수 구현
- REQ-FUNC-DIAG-003: 채점 로직을 순수 함수로 구현하여 동일 입력에 동일 점수를 보장

## Requirement Ref

- REQ-FUNC-DIAG-001 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-DIAG-003 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: SCR-002
- Route: —
- Page Entry: —

## Design Ref

- `design-reference/D-001/DESIGN.md` §3 type.score, §15, §17 Hero 높이
- `design-reference/UI_CONTRACT.md` SCR-002 주요 Component

## Depends On

- `FND-SECTIONS` — 공통 Section 컴포넌트(Intro·Hero·StepGuide·CtaBanner)

## Expected Files

- create: src/components/result/ScoreHero.tsx
- create: src/components/result/ScoreGauge.tsx
- create: src/components/result/InputSummary.tsx
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. Next.js 구현 전 `node_modules/next/dist/docs/` 관련 문서 확인(AGENTS.md)
2. `ScoreHero`는 100점 만점 총점을 `type.score`로 가장 크게 표시하고 점수 구간 코멘트를 함께 보여준다
3. `InputSummary`는 학력·나이·경력·자격증·skill 입력 요약을 항목별로 표시하며 미입력 선택 항목은 `없음`으로 표시한다

## Visual AC

1. Hero 높이 360~480px, 게이지와 점수 숫자가 같은 높이 범위에 있다
2. Desktop 좌우 분할 5:7, Mobile은 게이지→요약 순서 스택

## Security/Privacy AC

1. 동종 인원 대비 순위·백분위·공유 버튼을 만들지 않는다

## Test Cases

- REQ-FUNC-DIAG-001: TC-DIAG-001-N
- REQ-FUNC-DIAG-003: TC-DIAG-003-N

## Verify

- `npm run lint`, `npm run build`, `E2E-DIAG-FLOW`

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
