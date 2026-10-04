# TASK-DB-ACCESS DB 접근 함수(서버 전용)

- Task ID: DB-ACCESS
- Seq: 19
- Category: DB
- Priority: P0
- Status: NOT_STARTED

## Context

DB 접근 함수(서버 전용). 관리형 DB의 4개 테이블 범위 안에서 스키마·접근 제어·접근 함수를 만든다.

선행 Task: `DB-RLS-BASE`, `LIB-DEDUCTION-REASONS`, `LIB-RECO-MAPPER`.

이 Task에 의존하는 Task: `API-DIAG-SUBMIT`, `API-DIAG-RESULT`, `API-DIAG-REASONS`, `API-DIAG-RECOMMENDATIONS`, `API-DIAG-JOBS`, `TEST-RLS-BASIC`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-DIAG-003: 채점 로직을 순수 함수로 구현하여 동일 입력에 동일 점수를 보장
- REQ-NFR-SEC-002: 표준 인증/네트워크 접근 제어(DB 접근 키 관리, 환경변수 분리)로 제3자 무단 접근 차단

## Requirement Ref

- REQ-FUNC-DIAG-003 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-NFR-SEC-002 (IMPLEMENT) — SRS §4.4.3 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: —
- Route: —
- Page Entry: —

## Design Ref

- `docs/06_SRS_UIUX_REVISED.md` §4.2 핵심 데이터 엔터티 — 시각 규칙 없음

## Depends On

- `DB-RLS-BASE` — DB 접근 제어(RLS·서버 전용 키)
- `LIB-DEDUCTION-REASONS` — 감점 근거 도출
- `LIB-RECO-MAPPER` — 감점 항목 기반 추천 매핑

## Expected Files

- create: src/lib/db/client.ts
- create: src/lib/db/diagnosis-repo.ts
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. Next.js 구현 전 `node_modules/next/dist/docs/` 관련 문서 확인(AGENTS.md)
2. `saveDiagnosis(input, result, deductions, recommendations)`가 4개 테이블에 저장하고 `result_id`를 반환한다
3. `getDiagnosisById(result_id)`는 존재하지 않는 ID에 `null`을 반환한다
4. 모듈은 `server-only`로 선언해 클라이언트 번들에 포함되지 않는다

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. 서버 전용 키는 이 모듈 안에서만 읽는다
2. 질의는 필요한 컬럼만 선택하고 목록 전체 조회·검색 기능을 만들지 않는다(재조회는 `result_id` 단건)

## Test Cases

- REQ-FUNC-DIAG-003: TC-DIAG-003-N
- REQ-NFR-SEC-002: TC-NFR-SEC-002

## Verify

- `TEST-RLS-BASIC`, `npm run lint`, `npm run build`

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목을 모두 충족했다
- [ ] Verify의 명령·확인을 실행해 결과를 기록했다(통과하지 못하면 완료로 보고하지 않는다)
- [ ] Expected Files에 없는 파일을 수정하지 않았다
- [ ] Forbidden 항목에 해당하는 변경이 없다
- [ ] 테이블이 4개를 넘지 않는다(`diagnosis_inputs`, `diagnosis_results`, `deduction_items`, `recommendation_items`)

## Forbidden

- Expected Files 밖 파일 수정·생성 금지(필요하면 먼저 `TASKS/00_TASK_LIST.md`를 고친다)
- 로그인·계정·관리자·결제·별점·광고 UI·Route 추가 금지
- D-001 Token에 없는 색·간격·그림자 추가 금지
- `Lorem ipsum`·`준비 중`·`정보 확인 필요`·`TBD` 등 Placeholder 문구 금지
- 자동 Merge·EC2·AWS 설정 추가 금지
- 구현 코드·Branch·Commit을 이 문서 작업으로 만들지 않는다
- 4개 테이블 밖의 테이블·계정·결제 테이블 추가 금지
- 희망 직무 컬럼(`desired_job`)은 결정 D-02 전까지 추가 금지
- `priority_order` 사용 로직 금지
