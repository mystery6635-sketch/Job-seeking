# TASK-FEAT-OBS-EVENTS KPI 이벤트 기록(진단 완료·근거 화면 도달)

- Task ID: FEAT-OBS-EVENTS
- Seq: 26
- Category: API
- Priority: P1
- Status: NOT_STARTED

## Context

KPI 이벤트 기록(진단 완료·근거 화면 도달). 서버 Route Handler(또는 이벤트 기록)를 만든다.

선행 Task: `FND-SESSION-GUARD`.

이 Task에 의존하는 Task: `CMP-DIAG-FORM`, `CMP-REASON-DRAWER`, `PAGE-SCR001`, `PAGE-SCR002`, `MANUAL-LOGS-OBS`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-NFR-OBS-001: 무료 분석 도구로 진단 완료·근거 화면 도달 이벤트만 최소 기록(Dummy)

## Requirement Ref

- REQ-NFR-OBS-001 (IMPLEMENT) — SRS §4.4.4 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: SCR-001, SCR-002
- Route: —
- Page Entry: —

## Design Ref

- `docs/06_SRS_UIUX_REVISED.md` §6.1 Internal API Operations — 시각 규칙 없음

## Depends On

- `FND-SESSION-GUARD` — 진단 세션 저장소와 미완료 접근 Guard

## Expected Files

- create: src/lib/analytics.ts
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. Next.js 구현 전 `node_modules/next/dist/docs/` 관련 문서 확인(AGENTS.md)
2. 무료 분석 도구(Vercel Analytics 기본 기능)로 `diagnosis_completed`, `reasons_viewed` 두 이벤트만 기록한다(커스텀 로그 시스템 없음)
3. 이벤트 전송 실패는 사용자 흐름을 막지 않는다

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. 이벤트 payload에 입력값·점수·`result_id`를 넣지 않는다

## Test Cases

- REQ-NFR-OBS-001: TC-NFR-OBS-001-DRAFT

## Verify

- `MANUAL-LOGS-OBS`에서 이벤트 수신 확인

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
- 서버 멱등키·커스텀 감사 로그 시스템 추가 금지
- 요청 본문·개인정보 원문 로그 출력 금지
