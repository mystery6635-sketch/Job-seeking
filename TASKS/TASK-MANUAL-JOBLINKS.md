# TASK-MANUAL-JOBLINKS 구인 사이트 검색 URL 실사이트 확인

- Task ID: MANUAL-JOBLINKS
- Seq: 52
- Category: MANUAL
- Priority: P1
- Status: NOT_STARTED

## Context

구인 사이트 검색 URL 실사이트 확인. 자동화하지 않는 항목을 수동으로 확인하고 증거를 남긴다.

선행 Task: `DATA-JOBSITES`, `CMP-JOB-SITES`.

이 Task에 의존하는 Task: `RELEASE-CHECK`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-JOBLINK-001: 희망 직무 문자열을 사이트별 검색 URL 템플릿에 치환해 잡코리아·사람인·원티드·워크넷·IT 전문 구인 사이트 링크를 새 탭으로 연결(매칭·추천 로직 없음)

## Requirement Ref

- REQ-FUNC-JOBLINK-001 (IMPLEMENT) — SRS §4.3.3b (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: —
- Route: —
- Page Entry: —

## Design Ref

- `docs/06_SRS_UIUX_REVISED.md` §4.3.3b — 시각 규칙 없음

## Depends On

- `DATA-JOBSITES` — 외부 구인 사이트 검색 URL 템플릿 정적 데이터
- `CMP-JOB-SITES` — 구인 사이트 연결 Card Grid

## Expected Files

- create: TASKS/evidence/joblinks-check.md
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. 6개 사이트 링크를 실제로 열어 희망 직무 검색 결과 페이지로 이동하는지 확인하고 깨진 템플릿은 `DATA-JOBSITES`를 수정한다

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. 해당 없음

## Test Cases

- REQ-FUNC-JOBLINK-001: TC-JOBLINK-001-N
- 이 Task가 수행하는 케이스: Functional AC 각 항목

## Verify

- 수동 확인

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목을 모두 충족했다
- [ ] Verify의 명령·확인을 실행해 결과를 기록했다(통과하지 못하면 완료로 보고하지 않는다)
- [ ] Expected Files에 없는 파일을 수정하지 않았다
- [ ] Forbidden 항목에 해당하는 변경이 없다
- [ ] `TASKS/evidence/`에 확인 결과를 기록했다

## Forbidden

- Expected Files 밖 파일 수정·생성 금지(필요하면 먼저 `TASKS/00_TASK_LIST.md`를 고친다)
- 로그인·계정·관리자·결제·별점·광고 UI·Route 추가 금지
- D-001 Token에 없는 색·간격·그림자 추가 금지
- `Lorem ipsum`·`준비 중`·`정보 확인 필요`·`TBD` 등 Placeholder 문구 금지
- 자동 Merge·EC2·AWS 설정 추가 금지
- 구현 코드·Branch·Commit을 이 문서 작업으로 만들지 않는다
