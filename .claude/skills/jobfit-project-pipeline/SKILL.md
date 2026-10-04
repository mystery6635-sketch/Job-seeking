---
name: jobfit-project-pipeline
description: JobFit(구직역량 진단 서비스) PRD/SRS에서 Task를 생성·상세화·감사하고 5개 Screen 개발을 Task 단위로 순차 지원하는 프로젝트 Skill. /gen-tasklist, /gen-task-details, /audit-tasks 실행 시, 또는 Task 생성·Page Owner·Expected Files·추적표·Task 구현 순서 작업을 할 때 사용한다.
---

# JobFit Project Pipeline

승인된 설계 문서를 구현 Task로 변환하고(`/gen-tasklist`, `/gen-task-details`), 감사하고(`/audit-tasks`), Task를 순서대로 구현할 때 지켜야 할 경계를 정한다. 문서 생성 단계에서는 앱 코드를 쓰지 않는다. 이 Skill은 루트 `CLAUDE.md`의 규칙과 같은 방향이며, 충돌하면 `CLAUDE.md`가 이긴다.

```
validate_inputs.py → /gen-tasklist → /gen-task-details → audit_tasks.py (/audit-tasks) → Task 순차 구현
```

## 상수

- `HARNESS_SCHEMA` = `jobfit-screen-route-v1` (`SCREEN_ROUTE_CONTRACT.json`의 `schema_version`과 같아야 한다)
- 출력 위치: Task List 정본 `TASKS/00_TASK_LIST.md`, 구현 Task별 상세 `TASKS/TASK-<Task ID>.md`(1:1), 감사 산출물 `TASKS/TASK_MANIFEST.csv`·`TASKS/TASK_AUDIT_REPORT.md`
- `/gen-tasklist`는 `TASKS/00_TASK_LIST.md`만, `/gen-task-details`는 `TASKS/TASK-<ID>.md`만 작성한다. 구현 코드·Branch·Commit·Issue를 만들지 않는다.

## 1. 입력 문서 목록

| 파일 | 용도 |
|---|---|
| `docs/06_SRS_UIUX_REVISED.md` | SRS 정본: Requirement 명세, Acceptance Criteria, Release Criteria |
| `docs/PROJECT_SCOPE.md` | Scope 정본: Requirement별 IMPLEMENT / EXCLUDED, §6 확정된 결정·채점 구간표 |
| `docs/UIUX_TRACEABILITY.md` | Requirement·Screen·Route·Page Entry 연결, Test Case ID |
| `design-reference/D-001/DESIGN.md` | 디자인 정본(LOCKED): 시각 규칙, §19 화면별 Section 순서와 최소 콘텐츠 수 |
| `design-reference/UI_CONTRACT.md` | 화면별 영역·컴포넌트·상태·이동·금지 기능 |
| `design-reference/SCREEN_ROUTE_CONTRACT.json` | Screen 정본: Screen·Route·Page Entry·기술 Route·이동 관계 |
| `package.json`, `src/app` 실제 파일 트리 | 현재 상태 확인, Expected Files 기준 |
| `docs/ARCHITECTURE.md`, `docs/DECISION_LOG.md` | 구조 경계와 결정 기록 |

서로 충돌하면 위 정본이 이긴다. `design-reference/vendor/` 아래 파일은 참고용이다. 항상 `python scripts/validate_inputs.py`를 먼저 실행하고 실패하면 Task를 만들지 않는다.

## 2. 5개 Screen과 Page Entry

핵심 4개와 보조 1개이며 Page Owner Task는 Screen마다 정확히 하나다.

| Screen | 구분 | Route | Page Entry | Page Owner |
|---|---|---|---|---|
| SCR-001 진단 입력 | 핵심 | `/diagnosis` | `src/app/diagnosis/page.tsx` | `PAGE-SCR001` |
| SCR-002 역량리포트 | 핵심 | `/diagnosis/result` | `src/app/diagnosis/result/page.tsx` | `PAGE-SCR002` |
| SCR-003 직업훈련 추천 | 핵심 | `/diagnosis/result/recommendations` | `src/app/diagnosis/result/recommendations/page.tsx` | `PAGE-SCR003` |
| SCR-004 직무추천 | 핵심 | `/diagnosis/result/jobs` | `src/app/diagnosis/result/jobs/page.tsx` | `PAGE-SCR004` |
| SCR-005 직무수행태도 진단 | 보조 | `/diagnosis/attitude` | `src/app/diagnosis/attitude/page.tsx` | `PAGE-SCR005` |

- `/`(`src/app/page.tsx`)는 Screen이 아니라 `/diagnosis`로 redirect하는 기술 Route다. 이 파일을 다루는 Task는 하나이며(`FND-ROOT-REDIRECT`) AC에 "Next.js Starter 제거"와 "/diagnosis로 redirect"를 넣는다.
- 감점 근거는 SCR-002의 Drawer다. `/diagnosis/result/reasons` Route와 Page를 만들지 않는다.
- Page Entry를 새로 만들거나 Route를 바꾸려면 계약 JSON을 먼저 고친다.

## 3. IMPLEMENT·EXCLUDED 상태 처리 규칙

- `docs/PROJECT_SCOPE.md`의 모든 Requirement(현재 24개: REQ-FUNC 16, REQ-NFR 8)를 `00_TASK_LIST.md`의 "Requirement 추적표"에 IMPLEMENT 또는 EXCLUDED로 기록한다. PROJECT_SCOPE 상태와 다르게 적지 않는다.
- IMPLEMENT Requirement는 구현 Task(Category가 TEST·E2E·MANUAL이 아닌 것)와 Test/Manual Check Task에 모두 연결한다. 브라우저 확인이 필요한 항목은 `MANUAL` Task 또는 `RELEASE-CHECK`에 연결한다.
- EXCLUDED Requirement는 Task와 상세 파일을 만들지 않고, 추적표에서 지우지 않으며, `NON_IMPLEMENTATION` 표에 제외 근거와 후속 방향을 적는다.
- 구현하지 않은 것을 구현했다고 기록하지 않는다. 모든 Task의 시작 상태는 미착수다.
- 아직 확정되지 않은 결정은 임의로 확정하지 않고 `00_TASK_LIST.md`의 "가정과 확정된 결정" 표에 가정으로 남긴다. 확정된 결정은 `PROJECT_SCOPE.md` §6과 같아야 한다.

## 4. Task List·상세 Task 형식

문서 구성: 제목·메타 → `## 0. 요약`(Task 총 N개, Category별 수, Requirement 수) → `## 1. 가정과 확정된 결정` → `## 2. Task List` → `## 3. Screen ↔ Page Owner` → `## 4. Requirement 추적표` → `## 5. NON_IMPLEMENTATION` → `## 🔍 검증 체크`.

요약 형식(감사가 읽는다)
```
- Task 총 **56개** (개수는 완료 조건이 아니다)
- Category별: FOUNDATION 8, DATA 3, ...
```

Task List 표는 아래 16열이며 열 이름·순서가 정확히 같아야 한다.

```
| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files | Functional AC | Visual AC | Security/Privacy AC | Verify | Priority |
```

- Task ID·Requirement Ref·Route·Page Entry·Depends On·Expected Files의 각 값은 백틱으로 감싼다. 목록 값은 `<br>`로 구분하고 없으면 `—`를 쓴다.
- Expected Files는 `` `create 경로` ``, `` `modify 경로` ``, `` `delete 경로` `` 형식이며 실제 파일 트리를 확인해 쓴다(있으면 modify, 없으면 create).
- AC 셀의 여러 항목은 `1. … <br>2. …`로 구분한다. Implementation Status는 모두 `IMPLEMENT`다. Priority는 P0(Must·차단), P1(Should·검증), P2(보조)다.
- Task ID는 의미 있는 대문자 ID(`PAGE-SCR001`, `DATA-JOBSITES`, `UNIT-SCORING`)이며 Seq는 1부터 연속이다. 요약의 Task 수·Category별 수는 표와 일치해야 하고 개수는 완료 조건이 아니다(약 45~65개 예상). 한 Task는 하나의 검증 가능한 결과를 가진다.
- 코드 Task(`PAGE`, `COMPONENT`, `API`, `FOUNDATION`)의 Functional AC에는 "Next.js 구현 전 `node_modules/next/dist/docs/` 관련 문서 확인"을 넣는다.
- 시각 규칙은 D-001 Token만 쓴다. D-001에 없는 색·간격은 AC에서 요구하지 않는다.
- Requirement 추적표: `| Requirement | Status | 구현 Task | Test / Manual Check Task |`, NON_IMPLEMENTATION: `| Requirement | 제외 근거 | 후속 방향 |`

### Category

| Category | 용도 | 예 |
|---|---|---|
| `FOUNDATION` | 공통 기반 | 테스트 도구, Token CSS, 루트 Starter 제거, not-found, Header·Footer, Alert·Toast, 세션 Guard |
| `DATA` | `src/data` 정적 데이터 | 추천 매핑, 구인 사이트 URL 템플릿, MBTI 16유형 매핑 |
| `LOGIC` | 순수 함수 | 입력 검증, 점수 산출, 감점 근거, 추천 매핑, 링크 생성 |
| `DB` | 테이블·접근 | 4개 테이블 스키마, RLS, 접근 함수 |
| `API` | Route Handler, 이벤트 기록 | API-01~04, 06, 07 |
| `COMPONENT` | 화면용 컴포넌트 | ScoreGauge, ReasonDrawer, RecommendationCard, MbtiGrid |
| `PAGE` | Page Entry 소유·조립 | Screen마다 1개 |
| `TEST` / `E2E` | 단위·접근 제어 테스트 / Playwright | `UNIT-*`, `TEST-RLS-BASIC` / 2~3개 |
| `MANUAL` / `OPS` | 수동 확인·Release Check / CI·배포 점검 | `RELEASE-CHECK` / `OPS-CI` |

의존 순서: `FOUNDATION`·`DB`·`DATA` → `LOGIC` → `API`·`COMPONENT` → `PAGE` → `TEST`·`E2E` → `MANUAL`·`OPS`.

### 상세 파일 `TASKS/TASK-<Task ID>.md`

IMPLEMENT인 모든 Task마다 정확히 하나를 만든다. 같은 ID 파일이 있으면 갱신하고 중복 파일을 만들지 않는다. `python scripts/gen_task_details.py`가 Task List에서 결정적으로 생성한다.

- 사전 검사: 중복 ID, 빈 필수 열, 존재하지 않는 Depends On이 있으면 파일을 만들지 않는다.
- 절(순서 고정, 14개): Context, Project Scope, Requirement Ref, Screen / Route / Page Entry, Design Ref, Depends On, Expected Files, Functional AC, Visual AC, Security/Privacy AC, Test Cases, Verify, Definition of Done, Forbidden
- 값(Requirement Ref·Depends On·Expected Files·Page Entry·AC 항목 수)은 Task List 행과 같아야 한다. 바꿔야 하면 `00_TASK_LIST.md`를 먼저 고치고 다시 생성한다.
- Expected Files 절에 "Expected Files 밖 수정 금지"를 기록한다.

## 5. Page Owner·Component 분리 규칙

- Page Owner(`Category: PAGE`)는 Page Entry를 소유하고 Route Page 조립만 한다. Expected Files는 Page Entry 하나이며 하위 Component·API·Data 파일을 만들거나 수정하지 않는다.
- Component·API·Data Task는 Page Entry를 만들지 않는다. 하나의 Task가 여러 Page Entry를 소유하지 않는다.
- Page Owner는 같은 Screen의 모든 Component·API·Data Task에 의존한다. 다른 Page Owner에 의존하지 않으며 공유 코드는 Foundation·Component Task로 뺀다.
- "조립"은 import만이 아니라 화면 상태 전환까지 포함한다.
  - SCR-001: 필수·선택 Form, 3단계 안내, 제출 CTA. Starter 템플릿 사용 금지.
  - SCR-002: 점수 Hero·게이지·입력값 요약·카테고리 Chip·감점 근거 Drawer·진단 미완료 경고.
  - SCR-003: 추천 Card Grid ↔ 감점 없음 Empty State(상호 배타).
  - SCR-004: 구인 사이트 연결 Card Grid ↔ 희망 직무 없음 Empty State(상호 배타).
  - SCR-005: MBTI 16유형 그리드·태도 패널·미선택 Empty State·참고용 고지.
- Page Owner AC에는 다음을 모두 기록한다(`audit_tasks.py`가 검사).
  - `Section 순서`와 D-001 §19의 Screen별 Section 이름, `Section별 데이터 출처`
  - 최소 콘텐츠 수: SCR-001 필수 필드 3·선택 필드 2, SCR-002 카테고리 4, SCR-003 추천 Card 6개, SCR-004 연결 Card 6개, SCR-005 유형 Card 16개
  - 반응형 콘텐츠 밀도(Desktop·Mobile)
  - `Empty State`(아이콘·제목·설명·다음 행동 CTA 포함), `Lorem ipsum`·`준비 중`·`정보 확인 필요` 금지, `빈 영역` 금지, `Preview` 확인

## 6. DB 4개 Table과 정적 Data 경계

- DB는 4개 테이블로 제한한다: `diagnosis_inputs`, `diagnosis_results`, `deduction_items`, `recommendation_items`(SRS §4.2). 희망 직무는 `diagnosis_inputs.desired_job`(선택 컬럼)이며(D-02), 그 밖의 새 입력 컬럼·계정·결제·관리자 테이블은 만들지 않는다. 스키마·RLS·접근 함수는 별도 Task다.
- 추천 매핑, 구인 사이트 검색 URL 템플릿, MBTI 16유형 매핑, 채점 구간표는 `src/data`의 정적 TypeScript 데이터(`DATA` Task)다. 외부 연동·크롤링·공고 매칭·DB 시드 Task는 만들지 않는다(`DB-SEED-BASE`는 만들지 않는 결정 D-05).
- 점수·감점·검증·링크 생성은 순수 함수 `LOGIC` Task로 만들고 단위 테스트 Task에 연결한다. 점수는 `PROJECT_SCOPE.md` §6.1 구간표(4개 카테고리 균등 25점)를 따른다.
- 구인 사이트 연결은 희망 직무 문자열을 검색 URL 템플릿에 치환하는 데까지다. 공고 선별·정렬·추천·적합도 계산 Task는 없다.
- MBTI 지표는 핵심 100점과 합산하는 로직·표시를 만들지 않는다.

## 7. 외부 입력 비저장 불변조건

- 진단 입력(학력·나이·경력·자격증·skill·희망 직무)은 `POST /api/diagnosis`로만 서버(DB)에 보낸다. URL 쿼리·콘솔 로그·분석 이벤트로 보내지 않는다.
- 외부 구인 사이트에는 희망 직무 검색어만 URL에 담고, 학력·경력 등 다른 입력은 보내지 않으며, 외부 이동·클릭 기록을 서버·DB에 저장하지 않는다. 외부 링크는 새 탭에 `rel="noopener noreferrer"`를 가진다.
- 브라우저에는 `result_id`만 `sessionStorage`에 보관한다. KPI 이벤트(`diagnosis_completed`, `reasons_viewed`) payload에는 입력값·점수·`result_id`를 넣지 않는다.
- 이 조건은 `CMP-JOB-SITES`·`FEAT-OBS-EVENTS`·`FND-SESSION-GUARD` Task의 Security/Privacy AC에 반드시 있어야 하며 `audit_tasks.py` C13이 검사한다.

## 8. 인증·성인 확인·RLS 규칙

- v1에는 로그인·회원가입·계정·Auth·관리자 화면이 없다. 관련 Task·Route(`auth callback` 포함)를 만들지 않으며 Supabase Auth를 쓰지 않는다.
- 성인 확인·연령 인증 기능은 없다. 입력의 나이는 입력 검증에만 쓰고 점수에 반영하지 않는다.
- Supabase는 DB 용도만 쓴다. 4개 테이블 모두 RLS를 활성화하고 `anon`·`authenticated` 정책을 만들지 않으며, 서버 전용 service key로 Route Handler(서버 클라이언트)에서만 접근한다.
- 브라우저 Supabase 클라이언트와 RLS를 우회하는 Client 코드를 만들지 않는다. Service Role Key는 `NEXT_PUBLIC_` 없이 서버 환경변수로만 두고 `.env*`는 커밋하지 않는다.
- 저장 암호화는 Supabase 기본값, 접근 이력은 플랫폼 기본 로그로 대체한다. 보존기간은 90일이며 운영자가 수동 삭제한다(`PROJECT_SCOPE.md` §6.3).

## 9. Playwright Chromium 범위

- Playwright project는 `chromium` 하나다. Firefox·WebKit·부하 테스트 Task를 만들지 않는다.
- E2E Task는 2~3개로 묶는다. 현재는 `E2E-PUBLIC-SMOKE`(5개 Route·redirect·not-found), `E2E-DIAG-FLOW`, `E2E-JOBS-ATTITUDE`이며 Smoke Task(ID에 SMOKE)가 반드시 있다.
- E2E는 외부 사이트로 실제 이동하지 않고 `href`만 검증한다. CI에는 넣지 않고 수동으로 실행한다.

## 10. Task 순차 실행

개발 실행 단위는 Task다. `/run-wave`는 작성되어 있지만 Wave 구성(`TASKS/WAVE_PLAN.md`)이 아직 없다(결정 DEC-010·011). 그 파일이 생기기 전에는 Task 단위로 진행하고, 생긴 뒤에도 Wave 안에서 Task는 한 번에 하나씩 순서대로 구현한다.

1. `TASKS/TASK-<ID>.md`를 읽는다. `Depends On` Task가 완료됐는지 확인한다.
2. Task는 `Depends On` 순서로 한 번에 하나만 구현한다.
3. 현재 Task의 Expected Files 밖 파일은 수정하지 않는다. 필요하면 `00_TASK_LIST.md`를 먼저 고치고 상세 파일을 다시 생성한다.
4. Task 완료 순서: Task 읽기 → 입력 확인 → 구현 → 관련 포맷·Unit Test → 필요 시 Playwright → Diff 확인 → 완료 보고(변경 파일·검증 결과·남은 제한사항).
5. Page Owner가 끝나면 사람이 Desktop(1440)·Mobile(390) Preview를 확인한 뒤에 다음 Screen으로 넘어간다.
6. DB 연결이 필요한 Task는 `.env.local`의 Supabase 접속 정보가 없으면 막힌 것으로 보고하고 임의 값을 만들지 않는다.

## 11. EXCLUDED 보호

- EXCLUDED Requirement(`REQ-FUNC-PERSONALIZE-001~003`, `REQ-FUNC-ADMIN`, `REQ-NFR-AVAIL-001`, `REQ-NFR-PRIV-002`)에 대응하는 Task·상세 파일·UI·API·Route를 만들지 않는다. API-05(개인화 추천)와 관리자 화면, 자동 삭제 배치, 가동률 측정 도구가 해당한다.
- 로그인·결제·별점·광고·채용공고 매칭·커뮤니티·서버 멱등키·CMS·외부 Email 공급자·정식 Monitoring도 만들지 않는다.
- EXCLUDED를 구현 대상으로 바꾸려면 `PROJECT_SCOPE.md`와 SRS를 먼저 고치고 결정을 `docs/DECISION_LOG.md`에 새 ID로 기록한다. 감사(`audit_tasks.py` C17·C18)가 EXCLUDED 연결·상세 파일을 오류로 본다.

## 12. 금지: AWS·EC2·Prisma·자동 Merge

- AWS·EC2 Task·설정·파일을 만들지 않는다. 호스팅은 Vercel, DB는 Supabase다.
- Prisma·ORM을 추가하지 않는다. 마이그레이션은 `db/migrations/*.sql`로 관리한다.
- 자동 PR·자동 Merge·merge queue를 만들거나 실행하지 않는다. 허용되는 운영 Task는 CI(lint·typecheck·unit·build)와 Vercel 수동 배포·DB 연결 점검(`OPS`)뿐이다.
- destructive Git 명령을 임의로 쓰지 않는다. 커밋·push는 사용자가 요청할 때만 한다.

## 완료 조건

- `python scripts/validate_inputs.py` PASS
- `python scripts/audit_tasks.py` PASS(오류 0, `AUDIT_PASS checks=22`) — `TASKS/TASK_MANIFEST.csv`, `TASKS/TASK_AUDIT_REPORT.md` 갱신
- Page Owner 5개, Route·Page Entry 중복 없음, Requirement 24개 전부 추적표에 기록, 구현 Task ID와 `TASKS/TASK-*.md` 1:1
- 빠진 Requirement ID가 있으면 완료로 보고하지 않는다. 감사 실패 시 보고만 하지 말고 Task 문서를 고쳐 다시 감사한다.
