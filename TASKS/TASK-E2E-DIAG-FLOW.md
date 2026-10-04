# TASK-E2E-DIAG-FLOW Chromium 진단 핵심 흐름

- Task ID: E2E-DIAG-FLOW
- Seq: 48
- Category: E2E
- Priority: P0
- Status: NOT_STARTED

## Context

Chromium 진단 핵심 흐름. Playwright(Chromium)로 핵심 흐름을 확인한다.

선행 Task: `PAGE-SCR001`, `PAGE-SCR002`, `API-DIAG-SUBMIT`, `FND-TEST-TOOLING`.

이 Task에 의존하는 Task: `RELEASE-CHECK`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-DIAG-001: 학력·나이·경력·자격증·skill 입력을 받아 100점 만점 점수를 산출하는 결정적 채점 함수 구현
- REQ-FUNC-DIAG-002: 필수 항목(학력·나이·경력) 누락 시 점수 산출 이전에 검증하여 누락 항목을 명시한 오류 메시지 표시
- REQ-FUNC-DIAG-004: 진단 제출 시작 시 "진단하기" 버튼 비활성화, 응답 수신 후 재활성화(클라이언트 수준)
- REQ-FUNC-SCORE-001: 진단 완료 후 "근거 보기" 클릭 시 항목별 감점 사유를 최소 3개 이상 표시
- REQ-FUNC-SCORE-002: 만점 항목은 "감점 없음"으로 구분 표시
- REQ-FUNC-SCORE-003: 진단 미완료 상태에서 근거 화면 접근 시 "먼저 진단을 완료해주세요" 안내로 전환하고 접근 차단

## Requirement Ref

- REQ-FUNC-DIAG-001 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-DIAG-002 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-DIAG-004 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-SCORE-001 (IMPLEMENT) — SRS §4.3.2 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-SCORE-002 (IMPLEMENT) — SRS §4.3.2 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-SCORE-003 (IMPLEMENT) — SRS §4.3.2 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: —
- Route: —
- Page Entry: —

## Design Ref

- `docs/06_SRS_UIUX_REVISED.md` §4.3.1, §4.3.1, §4.3.1, §4.3.2, §4.3.2, §4.3.2 — 시각 규칙 없음

## Depends On

- `PAGE-SCR001` — 진단 입력 페이지 조립(Page Owner)
- `PAGE-SCR002` — 역량리포트 페이지 조립(Page Owner)
- `API-DIAG-SUBMIT` — POST /api/diagnosis (API-01)
- `FND-TEST-TOOLING` — 테스트 도구 설정(Vitest, Playwright Chromium)

## Expected Files

- create: tests/e2e/diag-flow.spec.ts
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. 정상 제출→점수 표시, 필수 누락→누락 항목 오류·점수 미표시, 제출 중 재클릭 시 추가 요청 1회만, `근거 보기` Drawer에 항목 4개와 Esc 닫기, 진단 미완료로 SCR-002·003·004 직접 접근 시 경고+SCR-001 CTA

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. 테스트 입력은 가상 데이터만 사용한다

## Test Cases

- REQ-FUNC-DIAG-001: TC-DIAG-001-N
- REQ-FUNC-DIAG-002: TC-DIAG-002-F
- REQ-FUNC-DIAG-004: TC-DIAG-004-N
- REQ-FUNC-SCORE-001: TC-SCORE-001-N
- REQ-FUNC-SCORE-002: TC-SCORE-002-N
- REQ-FUNC-SCORE-003: TC-SCORE-003-F
- 이 Task가 수행하는 케이스: Functional AC 각 항목

## Verify

- `npx playwright test --project=chromium tests/e2e/diag-flow.spec.ts`

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목을 모두 충족했다
- [ ] Verify의 명령·확인을 실행해 결과를 기록했다(통과하지 못하면 완료로 보고하지 않는다)
- [ ] Expected Files에 없는 파일을 수정하지 않았다
- [ ] Forbidden 항목에 해당하는 변경이 없다
- [ ] Chromium project에서만 실행해 통과한다

## Forbidden

- Expected Files 밖 파일 수정·생성 금지(필요하면 먼저 `TASKS/00_TASK_LIST.md`를 고친다)
- 로그인·계정·관리자·결제·별점·광고 UI·Route 추가 금지
- D-001 Token에 없는 색·간격·그림자 추가 금지
- `Lorem ipsum`·`준비 중`·`정보 확인 필요`·`TBD` 등 Placeholder 문구 금지
- 자동 Merge·EC2·AWS 설정 추가 금지
- 구현 코드·Branch·Commit을 이 문서 작업으로 만들지 않는다
- Firefox·WebKit project 추가 금지
- 외부 사이트로 실제 이동하는 검증 금지
