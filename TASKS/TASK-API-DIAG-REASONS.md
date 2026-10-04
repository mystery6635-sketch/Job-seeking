# TASK-API-DIAG-REASONS GET /api/diagnosis/[result_id]/reasons (API-03)

- Task ID: API-DIAG-REASONS
- Seq: 22
- Category: API
- Priority: P0
- Status: NOT_STARTED

## Context

GET /api/diagnosis/[result_id]/reasons (API-03). 서버 Route Handler(또는 이벤트 기록)를 만든다.

선행 Task: `DB-ACCESS`.

이 Task에 의존하는 Task: `CMP-REASON-DRAWER`, `PAGE-SCR002`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-SCORE-001: 진단 완료 후 "근거 보기" 클릭 시 항목별 감점 사유를 최소 3개 이상 표시
- REQ-FUNC-SCORE-002: 만점 항목은 "감점 없음"으로 구분 표시
- REQ-FUNC-SCORE-003: 진단 미완료 상태에서 근거 화면 접근 시 "먼저 진단을 완료해주세요" 안내로 전환하고 접근 차단

## Requirement Ref

- REQ-FUNC-SCORE-001 (IMPLEMENT) — SRS §4.3.2 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-SCORE-002 (IMPLEMENT) — SRS §4.3.2 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-SCORE-003 (IMPLEMENT) — SRS §4.3.2 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: SCR-002
- Route: `/api/diagnosis/[result_id]/reasons`
- Page Entry: `src/app/api/diagnosis/[result_id]/reasons/route.ts`

## Design Ref

- `docs/06_SRS_UIUX_REVISED.md` §6.1 Internal API Operations — 시각 규칙 없음

## Depends On

- `DB-ACCESS` — DB 접근 함수(서버 전용)

## Expected Files

- create: src/app/api/diagnosis/[result_id]/reasons/route.ts
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. Next.js 구현 전 `node_modules/next/dist/docs/` 관련 문서 확인(AGENTS.md)
2. 카테고리 4개 항목을 `status`·`reason_text`와 함께 반환한다(감점 없음 항목 포함)
3. 없는 `result_id`는 `404`와 진단 미완료 오류 코드를 반환한다

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. 응답 헤더에 `Cache-Control: no-store`를 지정한다

## Test Cases

- REQ-FUNC-SCORE-001: TC-SCORE-001-N
- REQ-FUNC-SCORE-002: TC-SCORE-002-N
- REQ-FUNC-SCORE-003: TC-SCORE-003-F

## Verify

- `npm run lint`, `npm run build`, 브라우저·curl 응답 확인

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
