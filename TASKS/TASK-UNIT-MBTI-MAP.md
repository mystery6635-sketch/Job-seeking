# TASK-UNIT-MBTI-MAP MBTI 매핑 단위 테스트

- Task ID: UNIT-MBTI-MAP
- Seq: 45
- Category: TEST
- Priority: P1
- Status: NOT_STARTED

## Context

MBTI 매핑 단위 테스트. 구현이 Requirement와 AC를 만족하는지 자동 테스트로 확인한다.

선행 Task: `DATA-MBTI-ATTITUDE`, `FND-TEST-TOOLING`.

이 Task에 의존하는 Task: `OPS-CI`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-ATTITUDE-001: MBTI 16유형별 직무 수행 태도 점수·강점·유의점 정적 매핑 조회, 핵심 점수와 분리 고지
- REQ-FUNC-ATTITUDE-002: MBTI 미선택 시 선택 유도 안내와 선택 UI 표시

## Requirement Ref

- REQ-FUNC-ATTITUDE-001 (IMPLEMENT) — SRS §4.3.3c (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-ATTITUDE-002 (IMPLEMENT) — SRS §4.3.3c (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: —
- Route: —
- Page Entry: —

## Design Ref

- `docs/06_SRS_UIUX_REVISED.md` §4.3.3c, §4.3.3c — 시각 규칙 없음

## Depends On

- `DATA-MBTI-ATTITUDE` — MBTI 16유형 직무 수행 태도 정적 데이터
- `FND-TEST-TOOLING` — 테스트 도구 설정(Vitest, Playwright Chromium)

## Expected Files

- create: tests/unit/mbti-map.test.ts
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. 16유형 전부가 존재하고 각각 강점 2개 이상·유의점 1개 이상이다(TC-ATTITUDE-001-N)
2. 알 수 없는 유형·미선택은 `null`을 반환한다(TC-ATTITUDE-002-F)

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. 매핑 모듈이 핵심 점수 모듈에 의존하지 않음을 import 검사로 확인한다

## Test Cases

- REQ-FUNC-ATTITUDE-001: TC-ATTITUDE-001-N
- REQ-FUNC-ATTITUDE-002: TC-ATTITUDE-002-F
- 이 Task가 수행하는 케이스: Functional AC 각 항목

## Verify

- `npm run test -- mbti-map`

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
