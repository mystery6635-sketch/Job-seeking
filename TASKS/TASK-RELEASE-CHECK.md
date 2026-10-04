# TASK-RELEASE-CHECK MVP Release Criteria 점검

- Task ID: RELEASE-CHECK
- Seq: 54
- Category: MANUAL
- Priority: P0
- Status: NOT_STARTED

## Context

MVP Release Criteria 점검. 자동화하지 않는 항목을 수동으로 확인하고 증거를 남긴다.

선행 Task: `MANUAL-PERF`, `MANUAL-PREVIEW`, `MANUAL-JOBLINKS`, `MANUAL-LOGS-OBS`, `E2E-PUBLIC-SMOKE`, `E2E-DIAG-FLOW`, `E2E-JOBS-ATTITUDE`, `OPS-CI`, `TEST-RLS-BASIC`.

이 Task에 의존하는 Task: 없음.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-DIAG-001: 학력·나이·경력·자격증·skill 입력을 받아 100점 만점 점수를 산출하는 결정적 채점 함수 구현
- REQ-FUNC-DIAG-002: 필수 항목(학력·나이·경력) 누락 시 점수 산출 이전에 검증하여 누락 항목을 명시한 오류 메시지 표시
- REQ-FUNC-DIAG-003: 채점 로직을 순수 함수로 구현하여 동일 입력에 동일 점수를 보장
- REQ-FUNC-DIAG-004: 진단 제출 시작 시 "진단하기" 버튼 비활성화, 응답 수신 후 재활성화(클라이언트 수준)
- REQ-FUNC-SCORE-001: 진단 완료 후 "근거 보기" 클릭 시 항목별 감점 사유를 최소 3개 이상 표시
- REQ-FUNC-SCORE-002: 만점 항목은 "감점 없음"으로 구분 표시
- REQ-FUNC-SCORE-003: 진단 미완료 상태에서 근거 화면 접근 시 "먼저 진단을 완료해주세요" 안내로 전환하고 접근 차단
- REQ-FUNC-RECO-001: `src/data` 하드코딩 정적 매핑 테이블로 감점 항목 기반 추천 리스트 제공, 감점 항목 없으면 대체 안내
- REQ-FUNC-JOBLINK-001: 희망 직무 문자열을 사이트별 검색 URL 템플릿에 치환해 잡코리아·사람인·원티드·워크넷·IT 전문 구인 사이트 링크를 새 탭으로 연결(매칭·추천 로직 없음)
- REQ-FUNC-JOBLINK-002: 희망 직무 정보 없음 시 안내 문구와 재진단 CTA 표시
- REQ-FUNC-ATTITUDE-001: MBTI 16유형별 직무 수행 태도 점수·강점·유의점 정적 매핑 조회, 핵심 점수와 분리 고지
- REQ-FUNC-ATTITUDE-002: MBTI 미선택 시 선택 유도 안내와 선택 UI 표시
- REQ-NFR-PERF-001: 진단 요청 후 5초 이내 결과 반환을 목표로 채점 로직을 동기·경량 함수로 구현
- REQ-NFR-SEC-001: 관리형 DB의 기본 저장 암호화 기능 활용, 커스텀 암호화 계층은 만들지 않음
- REQ-NFR-SEC-002: 표준 인증/네트워크 접근 제어(DB 접근 키 관리, 환경변수 분리)로 제3자 무단 접근 차단
- REQ-NFR-SEC-003: 커스텀 감사 로그 대신 호스팅/DB 플랫폼 기본 접근 로그 활용(Dummy)
- REQ-NFR-PRIV-001: 입력 폼을 진단에 필요한 항목(학력·나이·경력·자격증·skill)과 희망 직무로만 한정 설계
- REQ-NFR-OBS-001: 무료 분석 도구로 진단 완료·근거 화면 도달 이벤트만 최소 기록(Dummy)

## Requirement Ref

- REQ-FUNC-DIAG-001 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-DIAG-002 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-DIAG-003 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-DIAG-004 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-SCORE-001 (IMPLEMENT) — SRS §4.3.2 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-SCORE-002 (IMPLEMENT) — SRS §4.3.2 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-SCORE-003 (IMPLEMENT) — SRS §4.3.2 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-RECO-001 (IMPLEMENT) — SRS §4.3.3 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-JOBLINK-001 (IMPLEMENT) — SRS §4.3.3b (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-JOBLINK-002 (IMPLEMENT) — SRS §4.3.3b (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-ATTITUDE-001 (IMPLEMENT) — SRS §4.3.3c (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-ATTITUDE-002 (IMPLEMENT) — SRS §4.3.3c (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-NFR-PERF-001 (IMPLEMENT) — SRS §4.4.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-NFR-SEC-001 (IMPLEMENT) — SRS §4.4.3 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-NFR-SEC-002 (IMPLEMENT) — SRS §4.4.3 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-NFR-SEC-003 (IMPLEMENT) — SRS §4.4.3 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-NFR-PRIV-001 (IMPLEMENT) — SRS §4.4.3 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-NFR-OBS-001 (IMPLEMENT) — SRS §4.4.4 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: —
- Route: —
- Page Entry: —

## Design Ref

- `design-reference/D-001/DESIGN.md` §21 Do / Do Not, §22 검증 체크
- `design-reference/UI_CONTRACT.md` §0 공통 금지

## Depends On

- `MANUAL-PERF` — 응답 시간 수동 측정
- `MANUAL-PREVIEW` — Desktop·Mobile Preview 확인
- `MANUAL-JOBLINKS` — 구인 사이트 검색 URL 실사이트 확인
- `MANUAL-LOGS-OBS` — 저장 암호화·접근 로그·KPI 이벤트 확인
- `E2E-PUBLIC-SMOKE` — Chromium 공개 화면 Smoke
- `E2E-DIAG-FLOW` — Chromium 진단 핵심 흐름
- `E2E-JOBS-ATTITUDE` — Chromium 직무추천·태도 진단·Empty State
- `OPS-CI` — CI(lint·typecheck·unit·build)
- `TEST-RLS-BASIC` — DB 접근 제어 기본 테스트

## Expected Files

- create: TASKS/evidence/release-check.md
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. SRS §9.1~9.2·§9.5 체크리스트를 항목별로 통과/미통과로 기록하고 OQ-08·OQ-13·OQ-16·OQ-20 결정 여부를 확인한다
2. 로그인·관리자·결제·별점·광고 UI/Route가 없음을 코드 검색으로 확인한다
3. PRIV-002 임시 수동 삭제 SOP(보존 90일, PROJECT_SCOPE §6.3) 문서 존재를 확인한다(자동 삭제는 구현하지 않음)

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. 운영 키·개인정보가 저장소에 없음을 확인한다

## Test Cases

- REQ-FUNC-DIAG-001: TC-DIAG-001-N
- REQ-FUNC-DIAG-002: TC-DIAG-002-F
- REQ-FUNC-DIAG-003: TC-DIAG-003-N
- REQ-FUNC-DIAG-004: TC-DIAG-004-N
- REQ-FUNC-SCORE-001: TC-SCORE-001-N
- REQ-FUNC-SCORE-002: TC-SCORE-002-N
- REQ-FUNC-SCORE-003: TC-SCORE-003-F
- REQ-FUNC-RECO-001: TC-RECO-001-DRAFT
- REQ-FUNC-JOBLINK-001: TC-JOBLINK-001-N
- REQ-FUNC-JOBLINK-002: TC-JOBLINK-002-F
- REQ-FUNC-ATTITUDE-001: TC-ATTITUDE-001-N
- REQ-FUNC-ATTITUDE-002: TC-ATTITUDE-002-F
- REQ-NFR-PERF-001: TC-NFR-PERF-001
- REQ-NFR-SEC-001: TC-NFR-SEC-001
- REQ-NFR-SEC-002: TC-NFR-SEC-002
- REQ-NFR-SEC-003: TC-NFR-SEC-003
- REQ-NFR-PRIV-001: TC-NFR-PRIV-001
- REQ-NFR-OBS-001: TC-NFR-OBS-001-DRAFT
- 이 Task가 수행하는 케이스: Functional AC 각 항목

## Verify

- 체크리스트 기록

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
