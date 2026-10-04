# PROJECT_STATE — JobFit (구직역량 진단 서비스) v1 MVP

**기준일**: 2026-10-04
**성격**: 현재 진행 상태의 요약 스냅샷이다. 정본은 `TASKS/00_TASK_LIST.md`(Task), `TASKS/WAVE_STATE.json`(Wave·Task 진행, 아직 없음), `docs/PROJECT_SCOPE.md`(Scope), `docs/DECISION_LOG.md`(결정)이다. 이 문서의 값이 정본과 다르면 정본이 맞다. 아래 값은 모두 실제 파일에서 확인한 것이며 없는 것은 "없음"으로 적는다.

## 상태 요약

| 필드 | 값 |
|---|---|
| Harness Schema | `jobfit-screen-route-v1` |
| Design Version | D-001 (LOCKED, 2026-10-03) |
| Scope Mode | v1 MVP. Requirement 24개(IMPLEMENT 18, EXCLUDED 6), Task 56개 |
| Current Wave | 없음. `TASKS/WAVE_PLAN.md`가 없어 Wave가 정의되지 않았다(DEC-010·011 보류, `/run-wave`는 작성됨) |
| Current Task | 없음. 앱 구현 Task에 착수하지 않았다 |
| Completed Tasks | 0 / 56 (구현 Task 기준). Task 문서(목록·상세·감사)는 작성 완료, 앱 코드는 create-next-app 스캐폴드 그대로 |
| Blocked Tasks | 기록된 BLOCKED 없음(착수 전). 착수하면 막힐 Task는 아래 참조 |
| Latest CI | 없음. `.github/workflows/`가 없고 Git 원격 저장소가 없다 |
| Supabase State | 프로젝트·`.env.local` 없음. 4개 테이블 미생성, RLS 미적용 |
| Vercel Preview URL | 없음. Vercel 프로젝트 미연결 |
| Screen Checkpoints | 아래 표 (전부 PENDING) |
| Playwright State | 미설정. `package.json`에 `@playwright/test` 없음, E2E spec 0 / 3 |
| Deferred Items | 아래 목록 |
| Next Action | 아래 목록 |

## Screen Checkpoints

사람이 Desktop(1440)·Mobile(390) Preview를 확인한 결과를 기록한다. 확인 전에는 `PENDING`이다(상태 값: `PENDING`, `PASS`, `FAIL`).

| Screen | Route | Page Owner | 상태 |
|---|---|---|---|
| SCR-001 진단 입력 | `/diagnosis` | `PAGE-SCR001` | PENDING |
| SCR-002 역량리포트 | `/diagnosis/result` | `PAGE-SCR002` | PENDING |
| SCR-003 직업훈련 추천 | `/diagnosis/result/recommendations` | `PAGE-SCR003` | PENDING |
| SCR-004 직무추천 | `/diagnosis/result/jobs` | `PAGE-SCR004` | PENDING |
| SCR-005 직무수행태도 진단 | `/diagnosis/attitude` | `PAGE-SCR005` | PENDING |
| FINAL | 5개 Screen 전체 + Release Check | `MANUAL-PREVIEW`, `RELEASE-CHECK` | PENDING |

`/`는 Screen이 아니라 `/diagnosis`로 redirect하는 기술 Route라 Checkpoint 대상이 아니다.

## Blocked Tasks (착수하면 막힐 Task)

| Task | 필요한데 없는 것 |
|---|---|
| `DB-SCHEMA-BASE`(적용), `DB-RLS-BASE`, `DB-ACCESS`, `TEST-RLS-BASIC`, `API-DIAG-*`의 실제 호출, `MANUAL-LOGS-OBS` | Supabase 프로젝트와 `.env.local`(서버 전용 `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` — 제안 이름, `.env.example`에서 확정) |
| `OPS-CI`, `OPS-VERCEL-DB-CHECK` | GitHub 원격 저장소, Vercel 프로젝트 연결 |
| `MANUAL-*`, `RELEASE-CHECK` | `TASKS/evidence/`(아직 없음)와 사람의 확인 기록 |

UI·로직 Task(`FND-*`, `LIB-*`, `DATA-*`, `CMP-*`, `PAGE-*`)는 위 항목 없이 착수할 수 있다.

## Deferred Items

- Wave 구성(`TASKS/WAVE_PLAN.md`): DEC-010·011 보류. 정해지기 전에는 Task 단위로 진행한다.
- `result_id`의 `sessionStorage` 보관은 SRS에 방식이 없어 가정(A-01)이다.
- `DB-SEED-BASE` 미생성(D-05): 시드가 필요해지면 추가한다.
- SRS 미결: OQ-14(5초 초과 시 타임아웃 UX), OQ-18(오류 응답 스키마), OQ-19·21(감사 로그·KPI 항목)은 v1 임시 조치로 진행한다. 출시 차단 항목이 아니다.
- 디자인: `vendor/airbnb/DESIGN.md`가 지정돼 있으나 저장소에 없음, `04_UIUX_PLAN.md`의 액센트 색 표기 정정, Stitch SCR-004·SCR-005 브레드크럼 수동 수정(`DESIGN_MANIFEST.md` 미해결 사항).
- Post-MVP(EXCLUDED): 추천 개인화(`REQ-FUNC-PERSONALIZE-001~003`), 관리자 기능, 가동률 측정, 자동 삭제.
- 환경변수 이름 확정: `DB-RLS-BASE`가 `.env.example`을 만들 때 정한다.

## 저장소 상태

- 이전 커밋은 `83ebf71 backup: before finalizing open decisions`이다. 결정 확정·Task 감사·문서·Command·하네스 검증 스크립트 변경은 그 뒤에 한 커밋으로 묶었다(커밋 해시는 `git log`로 확인). Git 원격 저장소는 없다.
- `backup_20261004/`는 복사본이며 개발 대상이 아니다.
- 검증: `python scripts/validate_inputs.py` → `VALIDATE_INPUTS_PASS checks=42`, `python scripts/audit_tasks.py` → `AUDIT_PASS checks=22`. 감사는 문서 일관성만 검증하며 구현·테스트 통과를 뜻하지 않는다.

## Next Action

1. 작업 트리가 깨끗한지 확인한다. `prepare-task`는 깨끗한 작업 트리를 요구한다.
2. Wave를 쓸지 정한다. 쓰면 `TASKS/WAVE_PLAN.md`를 작성해 승인하고, 안 쓰면 Task 단위로 진행한다.
3. 첫 Task `FND-TEST-TOOLING`부터 `/prepare-task`로 점검한 뒤 `/implement-task`로 구현한다(의존 순서: `FND-*`·`DATA-*`·`DB-*` → `LIB-*` → `API-*`·`CMP-*` → `PAGE-*`).
4. 병행해서 Supabase 프로젝트, GitHub 원격 저장소, Vercel 프로젝트를 준비한다(DB·CI·배포 Task 착수 조건).
5. Page Owner가 하나 끝날 때마다 Preview를 확인하고 위 Screen Checkpoints 표를 갱신한다.

## 갱신 규칙

- 이 문서는 사람이 확인한 사실만 기록한다. 구현·검증하지 않은 것을 `DONE`·`PASS`로 쓰지 않는다.
- 값이 바뀌면 근거(커밋, 감사 결과, `TASKS/evidence/` 기록, 배포 URL)와 함께 고친다.
