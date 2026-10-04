# TASK-API-DIAG-SUBMIT POST /api/diagnosis (API-01)

- Task ID: API-DIAG-SUBMIT
- Seq: 20
- Category: API
- Priority: P0
- Status: NOT_STARTED

## Context

POST /api/diagnosis (API-01). 서버 Route Handler(또는 이벤트 기록)를 만든다.

선행 Task: `LIB-INPUT-VALIDATION`, `LIB-SCORING-ENGINE`, `LIB-DEDUCTION-REASONS`, `LIB-RECO-MAPPER`, `DB-ACCESS`.

이 Task에 의존하는 Task: `CMP-DIAG-FORM`, `PAGE-SCR001`, `E2E-DIAG-FLOW`, `MANUAL-PERF`, `OPS-VERCEL-DB-CHECK`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-DIAG-001: 학력·나이·경력·자격증·skill 입력을 받아 100점 만점 점수를 산출하는 결정적 채점 함수 구현
- REQ-FUNC-DIAG-002: 필수 항목(학력·나이·경력) 누락 시 점수 산출 이전에 검증하여 누락 항목을 명시한 오류 메시지 표시
- REQ-FUNC-DIAG-003: 채점 로직을 순수 함수로 구현하여 동일 입력에 동일 점수를 보장
- REQ-NFR-PERF-001: 진단 요청 후 5초 이내 결과 반환을 목표로 채점 로직을 동기·경량 함수로 구현
- REQ-NFR-SEC-001: 관리형 DB의 기본 저장 암호화 기능 활용, 커스텀 암호화 계층은 만들지 않음
- REQ-NFR-SEC-002: 표준 인증/네트워크 접근 제어(DB 접근 키 관리, 환경변수 분리)로 제3자 무단 접근 차단
- REQ-NFR-PRIV-001: 입력 폼을 진단에 필요한 항목(학력·나이·경력·자격증·skill)으로만 한정 설계

## Requirement Ref

- REQ-FUNC-DIAG-001 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-DIAG-002 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-DIAG-003 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-NFR-PERF-001 (IMPLEMENT) — SRS §4.4.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-NFR-SEC-001 (IMPLEMENT) — SRS §4.4.3 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-NFR-SEC-002 (IMPLEMENT) — SRS §4.4.3 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-NFR-PRIV-001 (IMPLEMENT) — SRS §4.4.3 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: SCR-001
- Route: `/api/diagnosis`
- Page Entry: `src/app/api/diagnosis/route.ts`

## Design Ref

- `docs/06_SRS_UIUX_REVISED.md` §6.1 Internal API Operations — 시각 규칙 없음

## Depends On

- `LIB-INPUT-VALIDATION` — 진단 입력 검증
- `LIB-SCORING-ENGINE` — 100점 진단 점수 산출 엔진
- `LIB-DEDUCTION-REASONS` — 감점 근거 도출
- `LIB-RECO-MAPPER` — 감점 항목 기반 추천 매핑
- `DB-ACCESS` — DB 접근 함수(서버 전용)

## Expected Files

- create: src/app/api/diagnosis/route.ts
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. Next.js 구현 전 `node_modules/next/dist/docs/` 관련 문서 확인(AGENTS.md)
2. 검증 실패 시 점수를 계산하지 않고 `400`과 누락 필드 목록을 반환한다
3. 성공 시 `result_id`를 반환하고 결과·감점·추천을 DB에 저장한다
4. 서버 멱등키 처리는 만들지 않는다(중복 방지는 클라이언트 버튼 비활성화로 한정)

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. 요청 본문 원문을 로그·에러 메시지에 남기지 않는다
2. 정의된 필드 외 입력은 무시한다(수집 범위 한정)

## Test Cases

- REQ-FUNC-DIAG-001: TC-DIAG-001-N
- REQ-FUNC-DIAG-002: TC-DIAG-002-F
- REQ-FUNC-DIAG-003: TC-DIAG-003-N
- REQ-NFR-PERF-001: TC-NFR-PERF-001
- REQ-NFR-SEC-001: TC-NFR-SEC-001
- REQ-NFR-SEC-002: TC-NFR-SEC-002
- REQ-NFR-PRIV-001: TC-NFR-PRIV-001

## Verify

- `npm run lint`, `npm run build`, 브라우저·curl 응답 확인

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목을 모두 충족했다
- [ ] Verify의 명령·확인을 실행해 결과를 기록했다(통과하지 못하면 완료로 보고하지 않는다)
- [ ] Expected Files에 없는 파일을 수정하지 않았다
- [ ] Forbidden 항목에 해당하는 변경이 없다
- [ ] 구현 전 `node_modules/next/dist/docs/` 관련 문서를 확인했다
- [ ] `npm run lint`·`npm run build`가 통과한다

## Forbidden

- Expected Files 밖 파일 수정·생성 금지(필요하면 먼저 `TASKS/00_TASK_LIST.md`를 고친다)
- 로그인·계정·관리자·결제·별점·광고 UI·Route 추가 금지
- D-001 Token에 없는 색·간격·그림자 추가 금지
- `Lorem ipsum`·`준비 중`·`정보 확인 필요`·`TBD` 등 Placeholder 문구 금지
- 자동 Merge·EC2·AWS 설정 추가 금지
- 구현 코드·Branch·Commit을 이 문서 작업으로 만들지 않는다
- 서버 멱등키·커스텀 감사 로그 시스템 추가 금지
- 요청 본문·개인정보 원문 로그 출력 금지
