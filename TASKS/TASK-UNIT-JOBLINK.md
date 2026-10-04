# TASK-UNIT-JOBLINK 구인 링크 생성 단위 테스트

- Task ID: UNIT-JOBLINK
- Seq: 44
- Category: TEST
- Priority: P1
- Status: NOT_STARTED

## Context

구인 링크 생성 단위 테스트. 구현이 Requirement와 AC를 만족하는지 자동 테스트로 확인한다.

선행 Task: `LIB-JOBLINK-BUILDER`, `FND-TEST-TOOLING`.

이 Task에 의존하는 Task: `OPS-CI`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-JOBLINK-001: 희망 직무 문자열을 사이트별 검색 URL 템플릿에 치환해 잡코리아·사람인·원티드·워크넷·IT 전문 구인 사이트 링크를 새 탭으로 연결(매칭·추천 로직 없음)
- REQ-FUNC-JOBLINK-002: 희망 직무 정보 없음 시 안내 문구와 재진단 CTA 표시

## Requirement Ref

- REQ-FUNC-JOBLINK-001 (IMPLEMENT) — SRS §4.3.3b (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-JOBLINK-002 (IMPLEMENT) — SRS §4.3.3b (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: —
- Route: —
- Page Entry: —

## Design Ref

- `docs/06_SRS_UIUX_REVISED.md` §4.3.3b, §4.3.3b — 시각 규칙 없음

## Depends On

- `LIB-JOBLINK-BUILDER` — 희망 직무 → 검색 링크 생성
- `FND-TEST-TOOLING` — 테스트 도구 설정(Vitest, Playwright Chromium)

## Expected Files

- create: tests/unit/joblinks.test.ts
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. 6개 사이트 링크가 모두 생성되고 한글·공백·특수문자 직무가 인코딩된다(TC-JOBLINK-001-N)
2. 빈 문자열·공백만 입력하면 빈 배열을 반환한다(TC-JOBLINK-002-F)

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. 모든 URL이 https 스킴이며 `javascript:` 입력이 URL 구조를 깨지 못한다

## Test Cases

- REQ-FUNC-JOBLINK-001: TC-JOBLINK-001-N
- REQ-FUNC-JOBLINK-002: TC-JOBLINK-002-F
- 이 Task가 수행하는 케이스: Functional AC 각 항목

## Verify

- `npm run test -- joblinks`

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
