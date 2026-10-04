# TASK-TEST-RLS-BASIC DB 접근 제어 기본 테스트

- Task ID: TEST-RLS-BASIC
- Seq: 46
- Category: TEST
- Priority: P0
- Status: NOT_STARTED

## Context

DB 접근 제어 기본 테스트. 구현이 Requirement와 AC를 만족하는지 자동 테스트로 확인한다.

선행 Task: `DB-RLS-BASE`, `DB-ACCESS`.

이 Task에 의존하는 Task: `RELEASE-CHECK`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-NFR-SEC-002: 표준 인증/네트워크 접근 제어(DB 접근 키 관리, 환경변수 분리)로 제3자 무단 접근 차단

## Requirement Ref

- REQ-NFR-SEC-002 (IMPLEMENT) — SRS §4.4.3 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: —
- Route: —
- Page Entry: —

## Design Ref

- `docs/06_SRS_UIUX_REVISED.md` §4.4.3 — 시각 규칙 없음

## Depends On

- `DB-RLS-BASE` — DB 접근 제어(RLS·서버 전용 키)
- `DB-ACCESS` — DB 접근 함수(서버 전용)

## Expected Files

- create: tests/unit/rls.test.ts
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. anon 키로 4개 테이블 select·insert가 거부되고 서버 경로(`DB-ACCESS`)로만 `result_id` 단건 조회가 된다
2. 존재하지 않는 `result_id`는 `null`을 반환한다

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. 테스트는 로컬/테스트용 DB 프로젝트만 대상으로 하며 운영 키를 쓰지 않는다

## Test Cases

- REQ-NFR-SEC-002: TC-NFR-SEC-002
- 이 Task가 수행하는 케이스: Functional AC 각 항목

## Verify

- `npm run test -- rls`(테스트 DB 환경변수 필요)

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목을 모두 충족했다
- [ ] Verify의 명령·확인을 실행해 결과를 기록했다(통과하지 못하면 완료로 보고하지 않는다)
- [ ] Expected Files에 없는 파일을 수정하지 않았다
- [ ] Forbidden 항목에 해당하는 변경이 없다
- [ ] 테스트가 현재 구현에서 통과한다

## Forbidden

- Expected Files 밖 파일 수정·생성 금지(필요하면 먼저 `TASKS/00_TASK_LIST.md`를 고친다)
- 로그인·계정·관리자·결제·별점·광고 UI·Route 추가 금지
- D-001 Token에 없는 색·간격·그림자 추가 금지
- `Lorem ipsum`·`준비 중`·`정보 확인 필요`·`TBD` 등 Placeholder 문구 금지
- 자동 Merge·EC2·AWS 설정 추가 금지
- 구현 코드·Branch·Commit을 이 문서 작업으로 만들지 않는다
- 운영 DB 키·실제 개인정보 사용 금지
