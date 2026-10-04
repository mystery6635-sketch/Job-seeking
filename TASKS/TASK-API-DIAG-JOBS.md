# TASK-API-DIAG-JOBS GET /api/diagnosis/[result_id]/jobs (API-06)

- Task ID: API-DIAG-JOBS
- Seq: 24
- Category: API
- Priority: P1
- Status: NOT_STARTED

## Context

GET /api/diagnosis/[result_id]/jobs (API-06). 서버 Route Handler(또는 이벤트 기록)를 만든다.

선행 Task: `DB-ACCESS`, `LIB-JOBLINK-BUILDER`.

이 Task에 의존하는 Task: `CMP-JOB-SITES`, `PAGE-SCR004`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-JOBLINK-001: 희망 직무 문자열을 사이트별 검색 URL 템플릿에 치환해 잡코리아·사람인·원티드·워크넷·IT 전문 구인 사이트 링크를 새 탭으로 연결(매칭·추천 로직 없음)
- REQ-FUNC-JOBLINK-002: 희망 직무 정보 없음 시 안내 문구와 재진단 CTA 표시

## Requirement Ref

- REQ-FUNC-JOBLINK-001 (IMPLEMENT) — SRS §4.3.3b (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-JOBLINK-002 (IMPLEMENT) — SRS §4.3.3b (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: SCR-004
- Route: `/api/diagnosis/[result_id]/jobs`
- Page Entry: `src/app/api/diagnosis/[result_id]/jobs/route.ts`

## Design Ref

- `docs/06_SRS_UIUX_REVISED.md` §6.1 Internal API Operations — 시각 규칙 없음

## Depends On

- `DB-ACCESS` — DB 접근 함수(서버 전용)
- `LIB-JOBLINK-BUILDER` — 희망 직무 → 검색 링크 생성

## Expected Files

- create: src/app/api/diagnosis/[result_id]/jobs/route.ts
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. Next.js 구현 전 `node_modules/next/dist/docs/` 관련 문서 확인(AGENTS.md)
2. `result_id` 유효성을 확인하고 사이트 목록을 반환한다. 희망 직무는 DB `diagnosis_inputs.desired_job`을 `result_id`로 읽어 링크를 치환한다(D-02 확정)
3. 희망 직무가 없으면 빈 링크 목록과 `empty: true`를 반환한다

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. 희망 직무 외에 새 입력 컬럼을 추가하지 않고, 사이트 목록·링크 응답에 다른 사용자의 데이터가 섞이지 않는다

## Test Cases

- REQ-FUNC-JOBLINK-001: TC-JOBLINK-001-N
- REQ-FUNC-JOBLINK-002: TC-JOBLINK-002-F

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
