# TASK-DB-SCHEMA-BASE DB 스키마(4개 테이블)

- Task ID: DB-SCHEMA-BASE
- Seq: 17
- Category: DB
- Priority: P0
- Status: NOT_STARTED

## Context

DB 스키마(4개 테이블). 관리형 DB의 4개 테이블 범위 안에서 스키마·접근 제어·접근 함수를 만든다.

선행 Task: `LIB-INPUT-VALIDATION`.

이 Task에 의존하는 Task: `DB-RLS-BASE`, `MANUAL-LOGS-OBS`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-NFR-SEC-001: 관리형 DB의 기본 저장 암호화 기능 활용, 커스텀 암호화 계층은 만들지 않음
- REQ-FUNC-DIAG-003: 채점 로직을 순수 함수로 구현하여 동일 입력에 동일 점수를 보장

## Requirement Ref

- REQ-NFR-SEC-001 (IMPLEMENT) — SRS §4.4.3 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-DIAG-003 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: —
- Route: —
- Page Entry: —

## Design Ref

- `docs/06_SRS_UIUX_REVISED.md` §4.2 핵심 데이터 엔터티 — 시각 규칙 없음

## Depends On

- `LIB-INPUT-VALIDATION` — 진단 입력 검증

## Expected Files

- create: db/migrations/001_base.sql
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. `diagnosis_inputs`, `diagnosis_results`, `deduction_items`, `recommendation_items` 4개 테이블만 만든다(SRS §4.2.2 ER 기준)
2. `result_id`는 추측 불가능한 UUID로 정의한다
3. 계정·사용자·결제·관리자 테이블과 `priority_order` 사용 로직을 만들지 않는다. `diagnosis_inputs`에 선택 컬럼 `desired_job`(text, null 허용)을 둔다(D-02 확정). 테이블은 4개를 유지한다

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. 관리형 DB의 기본 저장 암호화를 사용하고 커스텀 암호화 계층을 만들지 않는다(설정 확인은 `MANUAL-LOGS-OBS`)
2. 학력·나이·경력·자격증·skill·희망 직무 컬럼 외 개인정보 컬럼을 만들지 않는다

## Test Cases

- REQ-NFR-SEC-001: TC-NFR-SEC-001
- REQ-FUNC-DIAG-003: TC-DIAG-003-N

## Verify

- 마이그레이션 적용 후 테이블 4개 확인

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
- 희망 직무(`desired_job`) 외 입력 컬럼 추가 금지(결정 D-02)
- `priority_order` 사용 로직 금지
