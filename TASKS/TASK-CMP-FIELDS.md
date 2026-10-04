# TASK-CMP-FIELDS 입력 필드 컴포넌트(TextField·SelectField·ChipInput·NoneCheckbox)

- Task ID: CMP-FIELDS
- Seq: 27
- Category: COMPONENT
- Priority: P0
- Status: NOT_STARTED

## Context

입력 필드 컴포넌트(TextField·SelectField·ChipInput·NoneCheckbox). 화면에 쓰이는 컴포넌트를 만든다. Page Entry는 만들지 않는다.

선행 Task: `FND-TOKENS`, `FND-FEEDBACK`.

이 Task에 의존하는 Task: `CMP-DIAG-FORM`, `PAGE-SCR001`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-DIAG-002: 필수 항목(학력·나이·경력) 누락 시 점수 산출 이전에 검증하여 누락 항목을 명시한 오류 메시지 표시

## Requirement Ref

- REQ-FUNC-DIAG-002 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: SCR-001
- Route: —
- Page Entry: —

## Design Ref

- `design-reference/D-001/DESIGN.md` §10 Form · Tabs, §15 Desktop · Mobile 규칙, §20 placeholder 예시 값 규칙
- `design-reference/UI_CONTRACT.md` SCR-001 주요 Component

## Depends On

- `FND-TOKENS` — D-001 Token CSS와 루트 레이아웃
- `FND-FEEDBACK` — 공통 Alert·Toast·EmptyState·Skeleton

## Expected Files

- create: src/components/form/TextField.tsx
- create: src/components/form/SelectField.tsx
- create: src/components/form/ChipInput.tsx
- create: src/components/form/NoneCheckbox.tsx
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. Next.js 구현 전 `node_modules/next/dist/docs/` 관련 문서 확인(AGENTS.md)
2. ChipInput은 Chip 추가·삭제(키보드 Enter·Backspace 포함), `NoneCheckbox` 체크 시 입력을 `없음`으로 대체한다
3. 필드 오류는 필드 하단 `error` 메시지로 표시한다

## Visual AC

1. placeholder는 예시 값만 쓴다(예: `예: 컴퓨터활용능력 1급`), `입력하세요` 단독 문구 금지
2. 터치 영역 44px 이상, 포커스 링 2px accent

## Security/Privacy AC

1. `autocomplete`는 개인정보 자동완성을 유도하지 않도록 `off`로 지정한다

## Test Cases

- REQ-FUNC-DIAG-002: TC-DIAG-002-F

## Verify

- `npm run lint`, `npm run build`, 키보드만으로 Chip 추가·삭제

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
