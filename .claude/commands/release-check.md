---
description: v1 MVP 출시 가능 여부를 점검하고 RELEASE_READY 또는 RELEASE_BLOCKED로 판정한다. 파일을 수정하지 않고 배포·Merge도 하지 않는다
argument-hint: "(인자 없음)"
allowed-tools: Read, Grep, Glob, Bash(git status:*), Bash(git log:*), Bash(git remote:*), Bash(gh run list:*), Bash(gh pr checks:*), Bash(ls:*), Bash(npm run lint:*), Bash(npm run test:*), Bash(npm run build:*), Bash(npx tsc:*), Bash(npx playwright test:*)
---

`jobfit-project-pipeline` Skill과 루트 `CLAUDE.md`의 규칙을 따라 출시 점검을 한다. 기준은 `docs/06_SRS_UIUX_REVISED.md` §9(MVP Release Criteria)와 `TASKS/00_TASK_LIST.md`의 `RELEASE-CHECK` Task다.

이 Command는 **읽기와 검증 실행만 한다.** 소스·문서·Task 파일을 수정하지 않고, 배포·Commit·Push·PR·Merge를 하지 않으며, 감사·생성 스크립트(`audit_tasks.py`, `gen_task_details.py`)를 실행하지 않는다(문서를 다시 쓴다). 환경변수·키 값은 읽어도 출력하지 않는다. 기억이나 추정으로 통과를 판정하지 않고 실제 파일과 실행 결과로 판정한다.

## 점검

1. **Task·Wave 상태**
   - `TASKS/WAVE_STATE.json`이 있으면 그것을 정본으로 한다. `TASKS/00_TASK_LIST.md`의 구현 Task 56개가 모두 `DONE`이어야 하고 `PENDING`·`IN_PROGRESS`·`BLOCKED`·`FAILED`가 없어야 하며, 모든 Wave가 `DONE`(`WAITING_FOR_PREVIEW` 없음)이어야 한다.
   - 상태 파일이 없으면(Wave 미도입) 상태를 기록으로 확인할 수 없다. 이 경우 각 Task의 `create` 대상 파일이 모두 존재하는지와 아래 로컬 검증 결과로 대신하되, "상태 기록 없음"을 경고로 보고한다.
   - `MANUAL` Task는 `TASKS/evidence/`의 확인 기록이 있어야 완료로 본다.
2. **5개 Page Owner DONE**: `PAGE-SCR001`~`PAGE-SCR005`가 완료이고 5개 Page Entry(`SCREEN_ROUTE_CONTRACT.json`)가 실제로 존재한다. `src/app/page.tsx`에 create-next-app Starter 흔적(`next.svg`, `To get started`)이 없고 `/diagnosis`로 redirect한다. `/diagnosis/result/reasons` Page가 없다.
3. **CI PASS**: `.github/workflows/ci.yml`이 있고 lint·`tsc`·Vitest·build를 실행하는지 읽는다. Git 원격 저장소가 있으면 `gh run list`로 현재 커밋의 CI 결과가 성공인지 확인한다. 원격이 없거나 실행 기록이 없으면 CI PASS를 확인할 수 없는 것이다(통과로 추정하지 않는다). 로컬에서 `npm run lint`, `npx tsc --noEmit`, `npm run test -- --run`, `npm run build`를 실행해 결과를 함께 보고한다(CI 대체가 아니라 참고).
4. **Playwright Chromium PASS**: `playwright.config.ts`의 project가 `chromium` 하나뿐이고 E2E spec 3개(`public-smoke`, `diag-flow`, `jobs-attitude`)가 있다. `npx playwright test --project=chromium`을 실행해 Smoke를 포함한 전부 통과해야 한다. Firefox·WebKit이 설정에 있으면 실패다.
5. **Supabase 4개 Table·기본 RLS 확인 기록**:
   - `db/migrations/`가 `diagnosis_inputs`, `diagnosis_results`, `deduction_items`, `recommendation_items` 4개 테이블만 만들고(희망 직무는 `diagnosis_inputs.desired_job`), 4개 모두 RLS를 활성화하며 `anon`·`authenticated` 정책이 없다.
   - `TASKS/evidence/ops-check.md`와 `deploy-check.md`에 실제 Supabase 프로젝트의 테이블 4개·RLS 적용·저장 암호화·접근 로그 확인이 기록되어 있다. 기록이 없으면 확인되지 않은 것이다.
   - `TEST-RLS-BASIC` 테스트가 통과한다. 브라우저 Supabase 클라이언트가 없고 서버 전용 키에 `NEXT_PUBLIC_` 접두어가 없다.
6. **Vercel Preview Checkpoint**: `TASKS/evidence/preview-check.md`에 5개 Screen의 Desktop(1440)과 SCR-001·SCR-003의 Mobile(390) Preview 확인, 확인한 Vercel Preview URL, 확인 일시가 있고 Section 순서·최소 콘텐츠·Empty State·가로 스크롤 없음 항목이 체크되어 있다. `deploy-check.md`에 Vercel 수동 배포와 배포 URL에서 진단 제출→결과 조회가 동작한 기록이 있다. 사람이 확인한 기록이 없으면 통과가 아니다. 이 Command가 확인을 대신하지 않는다.
7. **EXCLUDED 목록**: `PROJECT_SCOPE.md`의 EXCLUDED 6개(`REQ-FUNC-PERSONALIZE-001~003`, `REQ-FUNC-ADMIN`, `REQ-NFR-AVAIL-001`, `REQ-NFR-PRIV-002`)가 `00_TASK_LIST.md`의 NON_IMPLEMENTATION 표에 모두 있고, 코드에 구현이 없다. 개인화 추천(API-05), 관리자 화면, 자동 삭제 배치, 가동률 측정 도구, 로그인·Auth·결제·별점·광고, Prisma·ORM, AWS·EC2 설정, 자동 Merge 설정이 `src/`, `db/`, `package.json`, `.github/`에 없다. 마지막 감사 결과(`TASKS/TASK_AUDIT_REPORT.md`)가 `AUDIT_PASS`인지 읽어서 확인한다.
8. **SRS §9 출시 조건**: PERF-001 5초 이내 측정 기록(`TASKS/evidence/perf-check.md`), 구인 사이트 링크 실제 확인 기록(`joblinks-check.md`), `TASKS/evidence/release-check.md`의 체크리스트가 있다. Release Blocking 결정(OQ-08·13·16·20)이 `PROJECT_SCOPE.md` §6에 확정되어 있다. REQ-NFR-PRIV-002용 90일 수동 삭제 SOP 문서가 있다.
9. **Secret·작업 트리**: 저장소에 Secret(`service_role` 값, `eyJ`로 시작하는 JWT, `sk-`, 비밀번호 리터럴)이 없고 `.env*`가 `.gitignore`에 의해 제외된다. `git status --porcelain`이 비어 있다(커밋하지 않은 변경은 출시 대상이 아니다).

## 허용되는 위험 (차단 아님)

SRS §9.3의 조건부 허용은 차단 사유가 아니라 위험으로 보고한다: 가동률(`REQ-NFR-AVAIL-001`)을 실측할 수 없음, 자동 삭제 없이 운영자 수동 삭제로 대응(`REQ-NFR-PRIV-002`), 접근 로그·KPI가 플랫폼 기본 기능 수준(`REQ-NFR-SEC-003`, `REQ-NFR-OBS-001`). 이 항목들의 기록(SOP, 임시 관찰 방법)이 없으면 그 자체는 위험으로 적고 판정은 바꾸지 않는다.

## 판정

첫 줄에 아래 중 정확히 하나만 쓴다.

| 판정 | 조건 |
|---|---|
| `RELEASE_READY` | 점검 1~9가 모두 통과하고 확인하지 못한 항목이 없다 |
| `RELEASE_BLOCKED` | 하나라도 실패했거나, 증거가 없어 확인하지 못했다 |

확인하지 못한 항목은 통과로 추정하지 않고 `RELEASE_BLOCKED`로 둔다. 사람의 확인이 필요한 항목(Preview, 수동 측정, Supabase·Vercel 콘솔 확인)의 기록이 없으면 그 항목이 막힌 이유다.

이어서 다음을 보고한다.

- 점검 9개의 결과표(번호·항목·PASS/FAIL/미확인·근거 파일 또는 명령 결과 요약)
- `RELEASE_BLOCKED`이면 막은 항목과 해소 방법(필요한 사람의 조치, 선행 Task, 등록할 환경변수 이름)
- 허용되는 위험 목록과 출시 후 남는 제한사항
- 실행한 로컬 검증 명령과 결과(실행하지 못한 명령과 이유 포함)

`RELEASE_READY`는 출시 승인이나 배포 지시가 아니다. 배포·Merge는 사용자가 직접 한다.
