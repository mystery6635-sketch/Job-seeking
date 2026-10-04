# TASK-LIB-INPUT-VALIDATION 진단 입력 검증

- Task ID: LIB-INPUT-VALIDATION
- Seq: 12
- Category: LOGIC
- Priority: P0
- Status: NOT_STARTED

## Context

진단 입력 검증. UI와 무관한 순수 함수를 만들어 단위 테스트로 검증 가능하게 한다.

선행 Task: 없음.

이 Task에 의존하는 Task: `LIB-SCORING-ENGINE`, `DB-SCHEMA-BASE`, `API-DIAG-SUBMIT`, `CMP-DIAG-FORM`, `UNIT-VALIDATION`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-DIAG-002: 필수 항목(학력·나이·경력) 누락 시 점수 산출 이전에 검증하여 누락 항목을 명시한 오류 메시지 표시
- REQ-NFR-PRIV-001: 입력 폼을 진단에 필요한 항목(학력·나이·경력·자격증·skill)으로만 한정 설계

## Requirement Ref

- REQ-FUNC-DIAG-002 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-NFR-PRIV-001 (IMPLEMENT) — SRS §4.4.3 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: SCR-001
- Route: —
- Page Entry: —

## Design Ref

- `docs/06_SRS_UIUX_REVISED.md` §4.3.1, §4.4.3 — 시각 규칙 없음

## Depends On

- 없음

## Expected Files

- create: src/lib/diagnosis/types.ts
- create: src/lib/diagnosis/validate.ts
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. `validateDiagnosisInput`은 학력·나이·경력 누락을 점수 산출 이전에 검사하고 누락 필드 목록과 한국어 오류 문구(원인+해결 방법)를 반환한다
2. 자격증·skill이 비어 있으면 `없음`으로 정규화한다. 나이는 정수 범위 검증을 한다
3. 입력 타입은 학력·나이·경력·자격증·skill·희망 직무 외 필드를 갖지 않는다

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. 이름·연락처·이력서 파일 등 정의되지 않은 개인정보 필드를 타입에 추가하지 않는다

## Test Cases

- REQ-FUNC-DIAG-002: TC-DIAG-002-F
- REQ-NFR-PRIV-001: TC-NFR-PRIV-001

## Verify

- `UNIT-VALIDATION`

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
