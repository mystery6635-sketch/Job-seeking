# UI/UX Traceability — JobFit

**기준일**: 2026-10-03
**근거**: `docs/06_SRS_UIUX_REVISED.md`, `docs/PROJECT_SCOPE.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`

## 범례

| 열 | 값 |
|---|---|
| Implementation Status | `NOT_IMPLEMENTED` 코드가 아직 없음 / `EXCLUDED` v1에서 만들지 않음 |
| Task | Task 생성 전에는 `PENDING_TASK_GENERATION`. EXCLUDED 항목은 `N/A (EXCLUDED)` |
| Test | SRS에 정의된 Test Case ID. 테스트 코드는 아직 작성되지 않았다 |
| Status | `NOT_STARTED` 착수 전 / `EXCLUDED` 제외 |

현재 `src/app`에는 create-next-app 스타터(`layout.tsx`, `page.tsx`, `globals.css`)만 있다. 어떤 Requirement도 구현·검증되지 않았다.

## 1. Functional Requirements

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-DIAG-001 | NOT_IMPLEMENTED | SCR-001, SCR-002 | `/diagnosis`, `/diagnosis/result`, `/api/diagnosis` | `src/app/diagnosis/page.tsx`, `src/app/diagnosis/result/page.tsx`, `src/app/api/diagnosis/route.ts` | PENDING_TASK_GENERATION | TC-DIAG-001-N | NOT_STARTED |
| REQ-FUNC-DIAG-002 | NOT_IMPLEMENTED | SCR-001 | `/diagnosis` | `src/app/diagnosis/page.tsx` | PENDING_TASK_GENERATION | TC-DIAG-002-F | NOT_STARTED |
| REQ-FUNC-DIAG-003 | NOT_IMPLEMENTED | SCR-001, SCR-002 | `/diagnosis`, `/diagnosis/result`, `/api/diagnosis/[result_id]` | `src/app/diagnosis/page.tsx`, `src/app/diagnosis/result/page.tsx`, `src/app/api/diagnosis/[result_id]/route.ts` | PENDING_TASK_GENERATION | TC-DIAG-003-N | NOT_STARTED |
| REQ-FUNC-DIAG-004 | NOT_IMPLEMENTED | SCR-001 | `/diagnosis` | `src/app/diagnosis/page.tsx` | PENDING_TASK_GENERATION | TC-DIAG-004-N | NOT_STARTED |
| REQ-FUNC-SCORE-001 | NOT_IMPLEMENTED | SCR-002 (감점 근거 Drawer) | `/diagnosis/result`, `/api/diagnosis/[result_id]/reasons` | `src/app/diagnosis/result/page.tsx`, `src/app/api/diagnosis/[result_id]/reasons/route.ts` | PENDING_TASK_GENERATION | TC-SCORE-001-N | NOT_STARTED |
| REQ-FUNC-SCORE-002 | NOT_IMPLEMENTED | SCR-002 (감점 근거 Drawer) | `/diagnosis/result`, `/api/diagnosis/[result_id]/reasons` | `src/app/diagnosis/result/page.tsx`, `src/app/api/diagnosis/[result_id]/reasons/route.ts` | PENDING_TASK_GENERATION | TC-SCORE-002-N | NOT_STARTED |
| REQ-FUNC-SCORE-003 | NOT_IMPLEMENTED | SCR-002, SCR-003, SCR-004 | `/diagnosis/result`, `/diagnosis/result/recommendations`, `/diagnosis/result/jobs` | `src/app/diagnosis/result/page.tsx`, `src/app/diagnosis/result/recommendations/page.tsx`, `src/app/diagnosis/result/jobs/page.tsx` | PENDING_TASK_GENERATION | TC-SCORE-003-F | NOT_STARTED |
| REQ-FUNC-RECO-001 | NOT_IMPLEMENTED | SCR-003 | `/diagnosis/result/recommendations`, `/api/diagnosis/[result_id]/recommendations` | `src/app/diagnosis/result/recommendations/page.tsx`, `src/app/api/diagnosis/[result_id]/recommendations/route.ts` | PENDING_TASK_GENERATION | TC-RECO-001-DRAFT | NOT_STARTED |
| REQ-FUNC-JOBLINK-001 | NOT_IMPLEMENTED | SCR-004 | `/diagnosis/result/jobs`, `/api/diagnosis/[result_id]/jobs` | `src/app/diagnosis/result/jobs/page.tsx`, `src/app/api/diagnosis/[result_id]/jobs/route.ts` | PENDING_TASK_GENERATION | TC-JOBLINK-001-N | NOT_STARTED |
| REQ-FUNC-JOBLINK-002 | NOT_IMPLEMENTED | SCR-004 | `/diagnosis/result/jobs` | `src/app/diagnosis/result/jobs/page.tsx` | PENDING_TASK_GENERATION | TC-JOBLINK-002-F | NOT_STARTED |
| REQ-FUNC-ATTITUDE-001 | NOT_IMPLEMENTED | SCR-005 | `/diagnosis/attitude`, `/api/attitude` | `src/app/diagnosis/attitude/page.tsx`, `src/app/api/attitude/route.ts` | PENDING_TASK_GENERATION | TC-ATTITUDE-001-N | NOT_STARTED |
| REQ-FUNC-ATTITUDE-002 | NOT_IMPLEMENTED | SCR-005 | `/diagnosis/attitude` | `src/app/diagnosis/attitude/page.tsx` | PENDING_TASK_GENERATION | TC-ATTITUDE-002-F | NOT_STARTED |
| REQ-FUNC-PERSONALIZE-001 | EXCLUDED | 없음 | — | — | N/A (EXCLUDED) | TC-PERSONALIZE-001-N (Post-MVP 미실행) | EXCLUDED |
| REQ-FUNC-PERSONALIZE-002 | EXCLUDED | 없음 | — | — | N/A (EXCLUDED) | TC-PERSONALIZE-002-N (Post-MVP 미실행) | EXCLUDED |
| REQ-FUNC-PERSONALIZE-003 | EXCLUDED | 없음 | — | — | N/A (EXCLUDED) | TC-PERSONALIZE-003-F (Post-MVP 미실행) | EXCLUDED |
| REQ-FUNC-ADMIN | EXCLUDED | 없음 | — | — | N/A (EXCLUDED) | 없음 (요구사항 미작성) | EXCLUDED |

## 2. Non-Functional Requirements

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NFR-PERF-001 | NOT_IMPLEMENTED | SCR-001 | `/diagnosis`, `/api/diagnosis` | `src/app/diagnosis/page.tsx`, `src/app/api/diagnosis/route.ts` | PENDING_TASK_GENERATION | TC-NFR-PERF-001 | NOT_STARTED |
| REQ-NFR-AVAIL-001 | EXCLUDED | 없음 | — | — | N/A (EXCLUDED) | TC-NFR-AVAIL-001 (초안, 미실행) | EXCLUDED |
| REQ-NFR-SEC-001 | NOT_IMPLEMENTED | 비화면 | `/api/diagnosis` (저장 경로) | `src/app/api/diagnosis/route.ts` | PENDING_TASK_GENERATION | TC-NFR-SEC-001 | NOT_STARTED |
| REQ-NFR-SEC-002 | NOT_IMPLEMENTED | 비화면 | `/api/diagnosis/**` | `src/app/api/diagnosis/route.ts`, `src/app/api/diagnosis/[result_id]/route.ts` | PENDING_TASK_GENERATION | TC-NFR-SEC-002 | NOT_STARTED |
| REQ-NFR-SEC-003 | NOT_IMPLEMENTED | 비화면 | 호스팅·DB 기본 로그 | 해당 없음 (플랫폼 설정) | PENDING_TASK_GENERATION | TC-NFR-SEC-003 | NOT_STARTED |
| REQ-NFR-PRIV-001 | NOT_IMPLEMENTED | SCR-001 | `/diagnosis` | `src/app/diagnosis/page.tsx` | PENDING_TASK_GENERATION | TC-NFR-PRIV-001 | NOT_STARTED |
| REQ-NFR-PRIV-002 | EXCLUDED | 없음 | — | — | N/A (EXCLUDED) | TC-NFR-PRIV-002 (운영자 수동 SOP 확인) | EXCLUDED |
| REQ-NFR-OBS-001 | NOT_IMPLEMENTED | SCR-001, SCR-002 | `/diagnosis`, `/diagnosis/result` | `src/app/diagnosis/page.tsx`, `src/app/diagnosis/result/page.tsx` | PENDING_TASK_GENERATION | TC-NFR-OBS-001-DRAFT | NOT_STARTED |

## 3. UI Screen 단위 추적

| Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|
| SCR-001 | `/diagnosis` | `src/app/diagnosis/page.tsx` | PENDING_TASK_GENERATION | AC-UI-01, 02, 05, 06, 07, 14~18 | NOT_STARTED |
| SCR-002 | `/diagnosis/result` | `src/app/diagnosis/result/page.tsx` | PENDING_TASK_GENERATION | AC-UI-03, 08, 09, 13~18 | NOT_STARTED |
| SCR-003 | `/diagnosis/result/recommendations` | `src/app/diagnosis/result/recommendations/page.tsx` | PENDING_TASK_GENERATION | AC-UI-09, 10, 14~18 | NOT_STARTED |
| SCR-004 | `/diagnosis/result/jobs` | `src/app/diagnosis/result/jobs/page.tsx` | PENDING_TASK_GENERATION | AC-UI-09, 11, 14~18 | NOT_STARTED |
| SCR-005 | `/diagnosis/attitude` | `src/app/diagnosis/attitude/page.tsx` | PENDING_TASK_GENERATION | AC-UI-12, 13, 14~18 | NOT_STARTED |

AC-UI 항목은 `docs/05_UIUX_APPROVED.md` §6에 정의되어 있다. AC-UI-04(Header·Breadcrumb 일치)와 AC-UI-19(Release 조건 확인)는 5개 Screen 전체에 적용된다.

## 4. 커버리지 점검

| 항목 | 결과 |
|---|---|
| REQ-FUNC 행 | 16개 (IMPLEMENT 12, EXCLUDED 4) |
| REQ-NFR 행 | 8개 (IMPLEMENT 6, EXCLUDED 2) |
| 합계 | 24개. `docs/02_SRS_BASELINE.md`의 Requirement와 일치하며 삭제된 항목 없음 |
| Route 중복 | 없음 |
| Page Entry 중복 | 없음 (Screen 단위 5개 모두 고유) |
| Task | IMPLEMENT 항목 전부 `PENDING_TASK_GENERATION` |
| 구현·테스트 완료 항목 | 0개 |
