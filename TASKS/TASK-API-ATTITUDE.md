# TASK-API-ATTITUDE GET /api/attitude?mbti= (API-07)

- Task ID: API-ATTITUDE
- Seq: 25
- Category: API
- Priority: P1
- Status: NOT_STARTED

## Context

GET /api/attitude?mbti= (API-07). 서버 Route Handler(또는 이벤트 기록)를 만든다.

선행 Task: `DATA-MBTI-ATTITUDE`.

이 Task에 의존하는 Task: `CMP-ATTITUDE-PANEL`, `PAGE-SCR005`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-ATTITUDE-001: MBTI 16유형별 직무 수행 태도 점수·강점·유의점 정적 매핑 조회, 핵심 점수와 분리 고지
- REQ-FUNC-ATTITUDE-002: MBTI 미선택 시 선택 유도 안내와 선택 UI 표시

## Requirement Ref

- REQ-FUNC-ATTITUDE-001 (IMPLEMENT) — SRS §4.3.3c (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-ATTITUDE-002 (IMPLEMENT) — SRS §4.3.3c (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: SCR-005
- Route: `/api/attitude`
- Page Entry: `src/app/api/attitude/route.ts`

## Design Ref

- `docs/06_SRS_UIUX_REVISED.md` §6.1 Internal API Operations — 시각 규칙 없음

## Depends On

- `DATA-MBTI-ATTITUDE` — MBTI 16유형 직무 수행 태도 정적 데이터

## Expected Files

- create: src/app/api/attitude/route.ts
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. Next.js 구현 전 `node_modules/next/dist/docs/` 관련 문서 확인(AGENTS.md)
2. 16유형 중 하나면 태도 점수·강점·유의점을 반환하고, 없거나 알 수 없는 유형이면 `400`과 선택 유도 안내 코드를 반환한다
3. 응답에 핵심 100점·합산 점수 필드를 두지 않는다

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. DB 저장·계정 연동 없이 정적 매핑만 조회한다

## Test Cases

- REQ-FUNC-ATTITUDE-001: TC-ATTITUDE-001-N
- REQ-FUNC-ATTITUDE-002: TC-ATTITUDE-002-F

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
