# TASK-DATA-MBTI-ATTITUDE MBTI 16유형 직무 수행 태도 정적 데이터

- Task ID: DATA-MBTI-ATTITUDE
- Seq: 11
- Category: DATA
- Priority: P1
- Status: NOT_STARTED

## Context

MBTI 16유형 직무 수행 태도 정적 데이터. `src/data`의 하드코딩 정적 데이터를 만든다(외부 연동·DB 저장 없음).

선행 Task: 없음.

이 Task에 의존하는 Task: `API-ATTITUDE`, `CMP-MBTI-GRID`, `PAGE-SCR005`, `UNIT-MBTI-MAP`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-ATTITUDE-001: MBTI 16유형별 직무 수행 태도 점수·강점·유의점 정적 매핑 조회, 핵심 점수와 분리 고지
- REQ-FUNC-ATTITUDE-002: MBTI 미선택 시 선택 유도 안내와 선택 UI 표시

## Requirement Ref

- REQ-FUNC-ATTITUDE-001 (IMPLEMENT) — SRS §4.3.3c (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-ATTITUDE-002 (IMPLEMENT) — SRS §4.3.3c (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: SCR-005
- Route: —
- Page Entry: —

## Design Ref

- `design-reference/UI_CONTRACT.md` SCR-005
- `design-reference/D-001/DESIGN.md` §21 Do(참고용 고지)

## Depends On

- 없음

## Expected Files

- create: src/data/mbti-attitude.ts
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. 16유형 전부에 대해 태도 점수·강점(2개 이상)·유의점(1개 이상)을 `src/data` 정적 매핑으로 정의하고 유형 문자열 조회 함수 `getAttitude(type)`를 제공한다(알 수 없는 유형은 `null`)
2. 점수는 참고용이며 핵심 100점 계산 모듈을 import하지 않는다

## Visual AC

1. 16개 항목 모두 실제 한국어 문장이며 빈 값이 없다

## Security/Privacy AC

1. 합격·채용 가능성을 단정하는 문구를 쓰지 않는다

## Test Cases

- REQ-FUNC-ATTITUDE-001: TC-ATTITUDE-001-N
- REQ-FUNC-ATTITUDE-002: TC-ATTITUDE-002-F

## Verify

- `UNIT-MBTI-MAP`

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목을 모두 충족했다
- [ ] Verify의 명령·확인을 실행해 결과를 기록했다(통과하지 못하면 완료로 보고하지 않는다)
- [ ] Expected Files에 없는 파일을 수정하지 않았다
- [ ] Forbidden 항목에 해당하는 변경이 없다
- [ ] 대응 단위 테스트가 통과하고 빈 필드가 없다

## Forbidden

- Expected Files 밖 파일 수정·생성 금지(필요하면 먼저 `TASKS/00_TASK_LIST.md`를 고친다)
- 로그인·계정·관리자·결제·별점·광고 UI·Route 추가 금지
- D-001 Token에 없는 색·간격·그림자 추가 금지
- `Lorem ipsum`·`준비 중`·`정보 확인 필요`·`TBD` 등 Placeholder 문구 금지
- 자동 Merge·EC2·AWS 설정 추가 금지
- 구현 코드·Branch·Commit을 이 문서 작업으로 만들지 않는다
- 외부 데이터 연동·크롤링·공고 매칭·추천 로직 금지
