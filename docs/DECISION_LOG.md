# DECISION_LOG — JobFit (구직역량 진단 서비스) v1 MVP

**기록일**: 2026-10-04
**용도**: 문서만 봐서는 이유를 알기 어려운 결정을 한곳에 모은다. 상세 규칙은 각 근거 문서가 정본이며 이 문서는 그 위치를 가리킨다.
**상태 값**: `확정` 결정되어 문서·Task에 반영됨 / `보류` 이 프로젝트에 적용 여부가 정해지지 않음

| ID | 결정 | 상태 |
|---|---|---|
| DEC-001 | 실제 개발 루트는 `C:\AI_SERVICE\Job\app` | 확정 |
| DEC-002 | 디자인 Screen은 핵심 4개·보조 1개 | 확정 |
| DEC-003 | 감점 근거는 SCR-002 Drawer로 통합하고 별도 Route를 만들지 않음 | 확정 |
| DEC-004 | 추천·구인 사이트·MBTI·채점 구간표는 정적 TypeScript 데이터 | 확정 |
| DEC-005 | Supabase는 DB 용도만 사용하고 Auth는 쓰지 않음 | 확정 |
| DEC-006 | DB는 4개 Table로 제한 | 확정 |
| DEC-007 | 브라우저에는 `result_id`만 `sessionStorage`에 유지 | 확정(A-01은 가정) |
| DEC-008 | Airbnb `DESIGN.md`는 vendor 참고 지정값, D-001이 실제 정본 | 확정 |
| DEC-009 | Playwright는 Chromium만 사용, Smoke를 포함한 E2E 3개 | 확정 |
| DEC-010 | 사용자의 개발 실행 단위는 Wave | **보류**(명령 작성됨, Wave 구성 미정) |
| DEC-011 | Single Agent가 Wave 내부 Task를 순차 수행 | **보류**(`/run-wave`에 규칙 반영, Wave 구성 미정) |
| DEC-012 | PR·Merge는 사용자가 수동 수행 | 확정 |
| DEC-013 | EC2·AWS는 사용하지 않음 | 확정 |
| DEC-014 | 제외 기능은 EXCLUDED로 관리 | 확정 |
| DEC-015 | 채점은 4개 카테고리 균등 25점, 감점은 25 − 획득 점수 | 확정 |
| DEC-016 | 진단 입력·결과 보존기간은 90일, 운영자 수동 삭제 | 확정 |
| DEC-017 | 희망 직무는 `diagnosis_inputs.desired_job`에 저장 | 확정 |
| DEC-018 | Task 문서는 `TASKS/00_TASK_LIST.md`와 `TASKS/TASK-<ID>.md` 1:1로 관리 | 확정 |

DEC-015~018은 요청하신 목록 뒤에 이어서 기록한 이번 작업의 결정이다.

---

## DEC-001 실제 개발 루트는 `Job/app`

- **결정**: 앱 코드·`package.json`·`TASKS/`·`scripts/`·`design-reference/`는 `C:\AI_SERVICE\Job\app`에 둔다. 이 폴더가 Git 저장소 루트다.
- **근거**: `package.json`과 `src/app`이 이 폴더에 있다. `C:\AI_SERVICE\job\docs`에는 PRD·SRS 원본(`PRD_Job seeking.md`, `06_SRS_Job seeking.md`)만 있다. 같은 `AI_SERVICE` 아래 `traveler/app`은 다른 프로젝트라 개발 루트가 아니다.
- **영향**: 모든 경로·명령(`python scripts/audit_tasks.py` 등)은 `Job/app`에서 실행한다. `backup_20261004/`는 복사본이며 개발 대상이 아니다.

## DEC-002 Screen은 핵심 4개·보조 1개

- **결정**: SCR-001 진단 입력, SCR-002 역량리포트, SCR-003 직업훈련 추천, SCR-004 직무추천은 핵심, SCR-005 직무수행태도 진단(MBTI)은 보조다. 합계 5개이며 Page Owner Task도 5개다.
- **근거**: `design-reference/UI_CONTRACT.md` §0, `SCREEN_ROUTE_CONTRACT.json`(`schema_version: jobfit-screen-route-v1`), `DESIGN_MANIFEST.md`(2026-10-03 LOCKED).
- **영향**: Screen 목록의 정본은 계약 JSON이다. `/`는 Screen이 아니라 `/diagnosis`로 redirect하는 기술 Route다.

## DEC-003 감점 근거는 SCR-002 Drawer로 통합

- **결정**: 감점 근거는 별도 Route(`/diagnosis/result/reasons`) 없이 SCR-002 안의 Drawer(모바일은 하단 시트)로 제공한다. Traveler의 "한 Route에 여러 도구 통합"과 같은 방식이다.
- **근거**: `SCREEN_ROUTE_CONTRACT.json`의 `excluded_technical_routes`, SRS §3.6.
- **영향**: `ReasonDrawer`는 `PAGE-SCR002`가 조립한다. `reasons` Page Entry를 만들지 않는다.

## DEC-004 정적 TypeScript 데이터

- **결정**: 자격증·훈련 추천 매핑, 구인 사이트 검색 URL 템플릿, MBTI 16유형 매핑, 채점 구간표는 `src/data`에 하드코딩한다. 외부 데이터 연동·크롤링·DB 시드는 없다.
- **근거**: `PROJECT_SCOPE.md` §2, SRS OQ-11(Dummy 확정), `DB-SEED-BASE` 미생성 결정 D-05.
- **영향**: `DATA-RECOMMENDATIONS`, `DATA-JOBSITES`, `DATA-MBTI-ATTITUDE`, `LIB-SCORING-ENGINE`(`scoring-rules.ts`).

## DEC-005 Supabase는 DB 용도만

- **결정**: 관리형 DB는 Supabase(Postgres)이며 Auth는 쓰지 않는다. Traveler와 달리 로그인·계정·관리자 기능이 v1에 없다.
- **근거**: SRS §3.4 EXT-01(인증 위임은 Post-MVP), 범위 밖 OS-06, 결정 D-04(2026-10-04).
- **영향**: Server 클라이언트만 쓰고 Browser 클라이언트는 만들지 않는다. 자세한 내용은 `docs/ARCHITECTURE.md` §6.

## DEC-006 DB는 4개 Table

- **결정**: `diagnosis_inputs`, `diagnosis_results`, `deduction_items`, `recommendation_items`만 둔다(Traveler는 6개).
- **근거**: SRS §4.2.2 ER, `audit_tasks.py` C12.
- **영향**: 계정·결제·관리자 테이블과 `priority_order` 사용 로직을 만들지 않는다.

## DEC-007 브라우저에는 `result_id`만 유지

- **결정**: 브라우저의 `sessionStorage`에는 `result_id`만 둔다. 학력·경력·자격증·희망 직무 원문은 브라우저에 저장하지 않고, 진단 제출 시에만 API로 서버(DB)에 보낸다. Traveler의 "입력은 Browser Memory에만"과 다르다. 결과 재조회가 요구되기 때문이다(REQ-FUNC-DIAG-003).
- **근거**: `FND-SESSION-GUARD` Task, 가정 A-01. SRS가 보관 방식을 명시하지 않아 `sessionStorage`는 가정이다.
- **영향**: 입력·`result_id`는 URL·로그·분석 이벤트에 넣지 않는다(`docs/ARCHITECTURE.md` §4.3).
- **재검토 조건**: SRS가 다른 보관 방식을 정하면 `FND-SESSION-GUARD`만 수정한다.

## DEC-008 Airbnb `DESIGN.md`는 참고 지정값, D-001이 정본

- **결정**: 구현·검수는 `design-reference/D-001/DESIGN.md`만 기준으로 한다. 지정된 vendor 참고본 `vendor/airbnb/DESIGN.md`는 직접 구현 기준이 아니며 현재 저장소에도 없다.
- **근거**: `DESIGN_MANIFEST.md`(Vendor Reference 불일치 — 저장소에는 `vendor/apple/DESIGN-apple.md`, `vendor/jobfit/DESIGN.md`만 있음). 액센트 색은 승인된 Stitch 디자인 시스템 기준으로 Trust Blue를 채택했고 `04_UIUX_PLAN.md`의 코랄은 쓰지 않는다.
- **영향**: D-001은 `LOCKED`라 수정하지 않는다. 변경이 필요하면 `D-002/DESIGN.md`를 새로 만들고 Manifest의 Active 항목만 바꾼다. Airbnb 등 외부 서비스의 상표·로고·고유 문구는 쓰지 않는다.
- **미해결**: vendor 경로의 파일 부재와 04 문서의 색 표기는 `DESIGN_MANIFEST.md` 미해결 사항으로 남아 있다.

## DEC-009 Playwright는 Chromium만

- **결정**: Playwright project는 `chromium` 하나다. Firefox·WebKit·부하 테스트는 만들지 않는다. E2E Task는 3개(Smoke 1 + 진단 흐름 1 + 직무추천·태도 진단 1)이며 CI에서는 돌리지 않고 수동으로 실행한다.
- **근거**: `FND-TEST-TOOLING`, `E2E-PUBLIC-SMOKE`, `E2E-DIAG-FLOW`, `E2E-JOBS-ATTITUDE`, `audit_tasks.py` C15.
- **차이**: Traveler는 Smoke만 필수였지만, 여기서는 핵심 흐름 2개를 더해 E2E를 2~3개로 묶었다.

## DEC-010 개발 실행 단위는 Wave — 보류

- **상태**: 이 프로젝트에는 Wave 개념이 없다. `TASKS/`·`scripts/`·`.claude/`에 Wave 그룹, Wave 생성 스크립트, `run-wave` 명령이 없고 56개 Task는 Wave로 묶여 있지 않다(Traveler `traveler/app`에만 `build_waves.py`가 있다).
- **판단 필요**: Wave를 도입하려면 별도 결정이 필요하다. 도입하면 의존 순서(`FOUNDATION`·`DB`·`DATA` → `LOGIC` → `API`·`COMPONENT` → `PAGE` → `TEST`·`E2E` → `MANUAL`·`OPS`)에 따라 Task를 묶는 스크립트와 감사 규칙을 추가해야 한다.
- **진행(2026-10-04)**: `.claude/commands/run-wave.md`를 작성했다(`status`·`resume`·`dry-run` 포함). 다만 `TASKS/WAVE_PLAN.md`(Task를 Wave로 묶은 계획, 사람이 승인)가 없어서 명령은 아직 쓸 수 없다. Wave 구성이 정해지면 이 결정을 `확정`으로 바꾼다.
- **그때까지**: Task 단위(`TASKS/TASK-<ID>.md`)로 개발한다.

## DEC-011 Single Agent의 순차 수행 — 보류

- **상태**: DEC-010에 종속된다. Wave가 없으므로 "Wave 내부 순차 수행"은 정의할 수 없다.
- **현재 상태**: `/run-wave`가 Wave 안에서 Task를 `Depends On` 순서로 한 번에 하나씩 순차 구현하도록 규칙을 정했다. Wave 구성(DEC-010)이 정해지면 함께 확정한다.

## DEC-012 PR·Merge는 사용자가 수동 수행

- **결정**: PR 생성·검토·Merge는 사용자가 직접 한다. 자동 Merge, merge queue, Merge 자동화 도구를 쓰지 않는다. CI(GitHub Actions)는 lint·타입 검사·단위 테스트·build만 실행한다.
- **근거**: `OPS-CI` Task, `audit_tasks.py` C16(자동 Merge Task 0), `docs/ARCHITECTURE.md` §8.
- **영향**: 현재 Git 원격 저장소가 없어 PR 자체가 아직 불가능하다(`ARCHITECTURE.md` §9).

## DEC-013 EC2·AWS는 사용하지 않음

- **결정**: 호스팅은 Vercel, DB는 Supabase다. EC2·AWS Task·설정·파일을 만들지 않는다.
- **근거**: `audit_tasks.py` C16, `validate_inputs.py`(AWS·EC2가 활성 기술로 정의되지 않았는지 검사), `docs/ARCHITECTURE.md` §8.

## DEC-014 제외 기능은 EXCLUDED로 관리

- **결정**: 구현하지 않는 Requirement는 삭제하지 않고 `PROJECT_SCOPE.md`와 `TASKS/00_TASK_LIST.md`의 추적표에 `EXCLUDED`로 남긴다. 상세 구현 Task 파일은 만들지 않고, `NON_IMPLEMENTATION` 표에 제외 근거와 후속 방향을 적는다.
- **대상(6개)**: `REQ-FUNC-PERSONALIZE-001`~`003`, `REQ-FUNC-ADMIN`, `REQ-NFR-AVAIL-001`, `REQ-NFR-PRIV-002`.
- **근거**: `audit_tasks.py` C17(Task 또는 EXCLUDED 표에 존재), C18(EXCLUDED 상세 구현 파일 미생성).
- **그 밖 제외**: 로그인·인증, 유료 전환, 채용공고 매칭·추천, 커뮤니티, 정식 감사 로그·모니터링·부하 테스트, 서버 멱등키(`PROJECT_SCOPE.md` §3). CMS·외부 Email 공급자·Monitoring도 범위 밖이다.

## DEC-015 채점은 4개 카테고리 균등 25점

- **결정**: 학력·경력·자격증·스킬을 각 25점 만점으로 계산해 합한다(0~100). 감점은 25 − 카테고리 획득 점수이고, 사유 문장은 구간표의 다음 구간 기준을 안내한다. 나이는 점수에 반영하지 않는다.
- **확정일**: 2026-10-04 (OQ-08·OQ-13). 구간표 수치는 선택지에 없어 제가 제안했다.
- **근거·영향**: `PROJECT_SCOPE.md` §6.1(구간표), `LIB-SCORING-ENGINE`, `LIB-DEDUCTION-REASONS`, `UNIT-SCORING`. 값을 바꾸면 결과가 달라지므로 표를 먼저 고치고 테스트를 갱신한다(OQ-17).

## DEC-016 보존기간 90일

- **결정**: 진단 입력·결과는 90일 보관하고 경과분은 운영자가 DB 콘솔에서 수동 삭제한다. 자동 삭제는 만들지 않는다(REQ-NFR-PRIV-002는 EXCLUDED 유지).
- **확정일**: 2026-10-04 (OQ-20). 대안은 30일·7일이었다.
- **근거·영향**: `PROJECT_SCOPE.md` §6.3, `RELEASE-CHECK`에서 SOP 존재를 확인한다.

## DEC-017 희망 직무는 DB에 저장

- **결정**: `diagnosis_inputs.desired_job`(선택 컬럼)에 저장하고 API-06이 `result_id`로 읽어 구인 사이트 링크를 만든다. 테이블은 4개를 유지한다.
- **확정일**: 2026-10-04 (D-02). 대안은 `sessionStorage`에만 보관하는 안이었다.
- **근거·영향**: SRS §4.2.1 `DiagnosisInput`에 필드를 추가했고(v1.3), `DB-SCHEMA-BASE`·`API-DIAG-SUBMIT`·`API-DIAG-JOBS`에 반영했다. 희망 직무 외 입력 컬럼은 추가하지 않는다.

## DEC-018 Task 문서는 `TASKS/`에서 1:1로 관리

- **결정**: Task List의 정본은 `TASKS/00_TASK_LIST.md`(16열 표), 구현 Task마다 `TASKS/TASK-<ID>.md` 상세 파일이 정확히 하나씩 있다. `docs/tasks/`는 쓰지 않는다. 상세 파일은 `scripts/gen_task_details.py`가 Task List에서 생성하므로 값을 바꾸려면 목록을 먼저 고친다.
- **확정일**: 2026-10-04. 대안은 `docs/tasks/TASKLIST.md` 기준으로 목록을 맞추는 안이었다.
- **근거·영향**: `scripts/audit_tasks.py`(C01~C22)가 검사하고 `TASKS/TASK_MANIFEST.csv`, `TASKS/TASK_AUDIT_REPORT.md`를 갱신한다. `.claude/skills/jobfit-project-pipeline/SKILL.md`와 `.claude/commands/`가 같은 경로를 쓴다.

---

## 결정 변경 규칙

- 결정을 바꾸면 기존 항목을 지우지 않고 상태를 `대체됨`으로 바꾼 뒤 새 ID로 이유와 함께 기록한다.
- 결정이 `PROJECT_SCOPE.md`·SRS·Task에 영향을 주면 그 문서를 먼저 고치고 `python scripts/audit_tasks.py`로 통과를 확인한다.
