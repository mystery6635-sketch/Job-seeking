# TASK-CMP-DIAG-FORM 진단 입력 Form 컴포넌트

- Task ID: CMP-DIAG-FORM
- Seq: 28
- Category: COMPONENT
- Priority: P0
- Status: NOT_STARTED

## Context

진단 입력 Form 컴포넌트. 화면에 쓰이는 컴포넌트를 만든다. Page Entry는 만들지 않는다.

선행 Task: `CMP-FIELDS`, `LIB-INPUT-VALIDATION`, `API-DIAG-SUBMIT`, `FND-SESSION-GUARD`, `FEAT-OBS-EVENTS`.

이 Task에 의존하는 Task: `PAGE-SCR001`, `MANUAL-PERF`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-DIAG-001: 학력·나이·경력·자격증·skill 입력을 받아 100점 만점 점수를 산출하는 결정적 채점 함수 구현
- REQ-FUNC-DIAG-002: 필수 항목(학력·나이·경력) 누락 시 점수 산출 이전에 검증하여 누락 항목을 명시한 오류 메시지 표시
- REQ-FUNC-DIAG-004: 진단 제출 시작 시 "진단하기" 버튼 비활성화, 응답 수신 후 재활성화(클라이언트 수준)
- REQ-NFR-PRIV-001: 입력 폼을 진단에 필요한 항목(학력·나이·경력·자격증·skill)과 희망 직무로만 한정 설계
- REQ-NFR-PERF-001: 진단 요청 후 5초 이내 결과 반환을 목표로 채점 로직을 동기·경량 함수로 구현

## Requirement Ref

- REQ-FUNC-DIAG-001 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-DIAG-002 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-DIAG-004 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-NFR-PRIV-001 (IMPLEMENT) — SRS §4.4.3 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-NFR-PERF-001 (IMPLEMENT) — SRS §4.4.1 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: SCR-001
- Route: —
- Page Entry: —

## Design Ref

- `design-reference/D-001/DESIGN.md` §10 Form · Tabs, §14 Error, §15 Desktop · Mobile 규칙
- `design-reference/UI_CONTRACT.md` SCR-001 상태·금지 기능

## Depends On

- `CMP-FIELDS` — 입력 필드 컴포넌트(TextField·SelectField·ChipInput·NoneCheckbox)
- `LIB-INPUT-VALIDATION` — 진단 입력 검증
- `API-DIAG-SUBMIT` — POST /api/diagnosis (API-01)
- `FND-SESSION-GUARD` — 진단 세션 저장소와 미완료 접근 Guard
- `FEAT-OBS-EVENTS` — KPI 이벤트 기록(진단 완료·근거 화면 도달)

## Expected Files

- create: src/components/diagnosis/DiagnosisForm.tsx
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. Next.js 구현 전 `node_modules/next/dist/docs/` 관련 문서 확인(AGENTS.md)
2. 필수 3개(학력·나이·경력)와 선택 필드(자격증·skill·희망 직무)를 제공하고 누락 시 서버 호출 없이 누락 항목을 명시한다
3. 제출 중 `진단하기` 버튼을 비활성화하고 스피너를 표시하며 응답 후 재활성화한다(클라이언트 수준)
4. 성공 시 `result_id`를 `FND-SESSION-GUARD`의 session에 저장하고 SCR-002로 이동한다. 실패 시 `error` Alert와 `다시 시도` 버튼을 보여준다

## Visual AC

1. Desktop Form 1~2열, Mobile 1열·제출 버튼 폭 100%·높이 52px
2. 제출 중·실패·필수 누락 상태가 각각 구분되어 보인다

## Security/Privacy AC

1. 이름·연락처·이력서 업로드 입력을 만들지 않는다(REQ-NFR-PRIV-001)
2. 입력 원문을 `console`·URL에 노출하지 않는다

## Test Cases

- REQ-FUNC-DIAG-001: TC-DIAG-001-N
- REQ-FUNC-DIAG-002: TC-DIAG-002-F
- REQ-FUNC-DIAG-004: TC-DIAG-004-N
- REQ-NFR-PRIV-001: TC-NFR-PRIV-001
- REQ-NFR-PERF-001: TC-NFR-PERF-001

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
