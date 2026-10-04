# TASK-DATA-JOBSITES 외부 구인 사이트 검색 URL 템플릿 정적 데이터

- Task ID: DATA-JOBSITES
- Seq: 10
- Category: DATA
- Priority: P1
- Status: NOT_STARTED

## Context

외부 구인 사이트 검색 URL 템플릿 정적 데이터. `src/data`의 하드코딩 정적 데이터를 만든다(외부 연동·DB 저장 없음).

선행 Task: 없음.

이 Task에 의존하는 Task: `LIB-JOBLINK-BUILDER`, `PAGE-SCR004`, `MANUAL-JOBLINKS`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-JOBLINK-001: 희망 직무 문자열을 사이트별 검색 URL 템플릿에 치환해 잡코리아·사람인·원티드·워크넷·IT 전문 구인 사이트 링크를 새 탭으로 연결(매칭·추천 로직 없음)

## Requirement Ref

- REQ-FUNC-JOBLINK-001 (IMPLEMENT) — SRS §4.3.3b (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: SCR-004
- Route: —
- Page Entry: —

## Design Ref

- `design-reference/D-001/DESIGN.md` §21 Do Not(사이트 로고 이미지 금지)
- `design-reference/UI_CONTRACT.md` SCR-004

## Depends On

- 없음

## Expected Files

- create: src/data/job-sites.ts
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. 잡코리아·사람인·원티드·워크넷·프로그래머스 잡·로켓펀치 6개를 `src/data`에 정의하고 각 항목은 `name`, `description`, `url_template`(`{query}` 치환 자리)을 가진다
2. 공고 선별·정렬·적합도 필드를 두지 않는다(OS-03 경계)

## Visual AC

1. 사이트 로고 이미지를 사용하지 않는다(텍스트 Card)

## Security/Privacy AC

1. `url_template`은 https 외부 도메인만 허용한다. 실제 검색 파라미터는 `MANUAL-JOBLINKS`에서 사이트별로 열어 확인한다

## Test Cases

- REQ-FUNC-JOBLINK-001: TC-JOBLINK-001-N

## Verify

- `UNIT-JOBLINK`, `MANUAL-JOBLINKS`

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
