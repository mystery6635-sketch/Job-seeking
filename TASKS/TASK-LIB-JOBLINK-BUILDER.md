# TASK-LIB-JOBLINK-BUILDER 희망 직무 → 검색 링크 생성

- Task ID: LIB-JOBLINK-BUILDER
- Seq: 16
- Category: LOGIC
- Priority: P1
- Status: NOT_STARTED

## Context

희망 직무 → 검색 링크 생성. UI와 무관한 순수 함수를 만들어 단위 테스트로 검증 가능하게 한다.

선행 Task: `DATA-JOBSITES`.

이 Task에 의존하는 Task: `API-DIAG-JOBS`, `CMP-JOB-SITES`, `UNIT-JOBLINK`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-JOBLINK-001: 희망 직무 문자열을 사이트별 검색 URL 템플릿에 치환해 잡코리아·사람인·원티드·워크넷·IT 전문 구인 사이트 링크를 새 탭으로 연결(매칭·추천 로직 없음)
- REQ-FUNC-JOBLINK-002: 희망 직무 정보 없음 시 안내 문구와 재진단 CTA 표시

## Requirement Ref

- REQ-FUNC-JOBLINK-001 (IMPLEMENT) — SRS §4.3.3b (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-JOBLINK-002 (IMPLEMENT) — SRS §4.3.3b (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: SCR-004
- Route: —
- Page Entry: —

## Design Ref

- `docs/06_SRS_UIUX_REVISED.md` §4.3.3b, §4.3.3b — 시각 규칙 없음

## Depends On

- `DATA-JOBSITES` — 외부 구인 사이트 검색 URL 템플릿 정적 데이터

## Expected Files

- create: src/lib/diagnosis/joblinks.ts
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. `buildJobLinks(desiredJob)`는 각 사이트 `url_template`의 `{query}`에 `encodeURIComponent(trim(desiredJob))`를 치환한 목록을 반환한다. 정렬·필터·적합도 계산은 하지 않는다
2. 희망 직무가 비어 있으면 빈 배열을 반환한다(JOBLINK-002 분기)

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. 입력 문자열은 반드시 인코딩해 URL을 만들고 `javascript:` 등 비 https 스킴을 허용하지 않는다

## Test Cases

- REQ-FUNC-JOBLINK-001: TC-JOBLINK-001-N
- REQ-FUNC-JOBLINK-002: TC-JOBLINK-002-F

## Verify

- `UNIT-JOBLINK`

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목을 모두 충족했다
- [ ] Verify의 명령·확인을 실행해 결과를 기록했다(통과하지 못하면 완료로 보고하지 않는다)
- [ ] Expected Files에 없는 파일을 수정하지 않았다
- [ ] Forbidden 항목에 해당하는 변경이 없다
- [ ] 대응 단위 테스트가 통과한다

## Forbidden

- Expected Files 밖 파일 수정·생성 금지(필요하면 먼저 `TASKS/00_TASK_LIST.md`를 고친다)
- 로그인·계정·관리자·결제·별점·광고 UI·Route 추가 금지
- D-001 Token에 없는 색·간격·그림자 추가 금지
- `Lorem ipsum`·`준비 중`·`정보 확인 필요`·`TBD` 등 Placeholder 문구 금지
- 자동 Merge·EC2·AWS 설정 추가 금지
- 구현 코드·Branch·Commit을 이 문서 작업으로 만들지 않는다
- MBTI 지표를 핵심 100점과 합산하는 코드 금지
- 시간·난수·외부 호출에 의존하는 점수 계산 금지
