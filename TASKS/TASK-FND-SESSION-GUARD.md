# TASK-FND-SESSION-GUARD 진단 세션 저장소와 미완료 접근 Guard

- Task ID: FND-SESSION-GUARD
- Seq: 8
- Category: FOUNDATION
- Priority: P0
- Status: NOT_STARTED

## Context

진단 세션 저장소와 미완료 접근 Guard. 여러 Screen이 공유하는 기반을 만든다.

선행 Task: `FND-FEEDBACK`.

이 Task에 의존하는 Task: `FEAT-OBS-EVENTS`, `CMP-DIAG-FORM`, `PAGE-SCR002`, `PAGE-SCR003`, `PAGE-SCR004`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-SCORE-003: 진단 미완료 상태에서 근거 화면 접근 시 "먼저 진단을 완료해주세요" 안내로 전환하고 접근 차단

## Requirement Ref

- REQ-FUNC-SCORE-003 (IMPLEMENT) — SRS §4.3.2 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: SCR-002, SCR-003, SCR-004
- Route: —
- Page Entry: —

## Design Ref

- `design-reference/D-001/DESIGN.md` §13 Alert(warning), §14 Error(진단 미완료 접근)
- `design-reference/UI_CONTRACT.md` SCR-002~004 상태

## Depends On

- `FND-FEEDBACK` — 공통 Alert·Toast·EmptyState·Skeleton

## Expected Files

- create: src/lib/session.ts
- create: src/components/diagnosis/DiagnosisGuard.tsx
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. Next.js 구현 전 `node_modules/next/dist/docs/` 관련 문서 확인(AGENTS.md)
2. `result_id`만 브라우저 `sessionStorage`에 보관한다(탭 세션 단위, 계정·인증 쿠키 없음. 희망 직무는 DB에서 조회). 저장 방식은 SRS에 명시가 없어 가정으로 기록한다(§가정 A-01)
3. `DiagnosisGuard`는 `result_id`가 없거나 서버 조회가 404이면 `먼저 진단을 완료해주세요` WarningAlert와 SCR-001 이동 CTA를 보여주고 자식 콘텐츠를 렌더링하지 않는다
4. `sessionStorage` 접근 실패(try/catch) 시에도 Guard 상태로 안전하게 전환한다

## Visual AC

1. WarningAlert는 Section 상단 인라인, 좌측 4px 색 바, 아이콘+텍스트 병행

## Security/Privacy AC

1. `sessionStorage` 값은 `result_id`뿐이며 학력·경력·자격증·희망 직무 원문을 저장하지 않는다

## Test Cases

- REQ-FUNC-SCORE-003: TC-SCORE-003-F

## Verify

- 단위 테스트(session 함수) + `E2E-DIAG-FLOW`에서 미완료 접근 확인

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
