---
name: jobfit-project-pipeline
description: JobFit(구직역량 진단 서비스) 승인 Screen 5개와 SRS Requirement를 Next.js App Router 구현 Task List(TASKS/00_TASK_LIST.md)로 변환하고 감사한다. /gen-tasklist, /gen-task-details, /audit-tasks 실행 시, 또는 Task 생성·Page Owner·Expected Files·추적표 작업을 할 때 사용한다.
---

# JobFit Project Pipeline

승인된 설계 문서를 구현 Task로 변환하는 Pipeline이다. 이 Skill은 Task 문서만 만들며 앱 코드는 작성하지 않는다.

```
validate_inputs.py → /gen-tasklist → /gen-task-details → audit_tasks.py (/audit-tasks)
```

## 상수

- `HARNESS_SCHEMA` = `jobfit-screen-route-v1` (`SCREEN_ROUTE_CONTRACT.json`의 `schema_version`과 동일해야 한다)
- Screen 정본: `design-reference/SCREEN_ROUTE_CONTRACT.json`. 다른 문서와 충돌하면 이 파일이 이긴다.
- 출력 위치: Task List 정본 `TASKS/00_TASK_LIST.md`, 구현 Task별 상세 `TASKS/TASK-<Task ID>.md`(1:1).
- `/gen-tasklist`는 `TASKS/00_TASK_LIST.md`만, `/gen-task-details`는 `TASKS/TASK-<ID>.md`만 작성한다. 구현 코드·Branch·Commit·Issue를 만들지 않는다.

## 입력

| 파일 | 용도 |
|---|---|
| `docs/06_SRS_UIUX_REVISED.md` | Requirement 명세, Acceptance Criteria, Release Criteria |
| `docs/PROJECT_SCOPE.md` | Requirement별 IMPLEMENT / EXCLUDED 상태 |
| `docs/UIUX_TRACEABILITY.md` | Requirement·Screen·Route·Page Entry 연결 |
| `design-reference/D-001/DESIGN.md` | 시각 규칙, 화면별 Section 순서와 최소 콘텐츠 수 |
| `design-reference/UI_CONTRACT.md` | 화면별 영역·컴포넌트·상태·이동·금지 기능 |
| `design-reference/SCREEN_ROUTE_CONTRACT.json` | Screen·Route·Page Entry·기술 Route·이동 관계 |
| `package.json`, `src/app` 실제 파일 트리 | 현재 상태 확인, Expected Files 기준 |

## 핵심 규칙

**입력 검증**
1. 항상 `python scripts/validate_inputs.py`를 먼저 실행하고 실패하면 Task List를 만들지 않는다.
2. `src/app` 실제 파일 트리를 확인한 뒤 Expected Files를 쓴다. 이미 있는 파일은 `modify`, 없는 파일은 `create`, 없애는 파일은 `delete`로 쓴다.

**Screen과 Page Owner**
3. Screen은 정확히 5개(SCR-001~005)이며 각각 Page Owner Task(`Category: PAGE`)를 하나만 만든다. Page Owner의 Expected Files에는 해당 `page_entry`가 들어간다.
4. Page Owner와 Component Task를 구분한다. Component·API·Data Task는 Page Entry를 만들지 않는다.
5. Page Owner는 같은 Screen의 모든 Component·API·Data Task에 의존한다. 다른 Page Owner에 의존하지 않으며 공유 코드는 Foundation·Component Task로 뺀다.
6. 하나의 Task가 여러 Page Entry를 소유하지 않는다. `src/app/page.tsx`를 다루는 Task는 하나이며 AC에 "Next.js Starter 제거"와 "/diagnosis로 redirect"를 넣는다. `/`는 Screen이 아닌 기술 Route다.
7. SCR-001 Owner AC에는 Starter 템플릿 사용 금지를 넣는다.
8. SCR-002 Owner는 점수 Hero·게이지·카테고리 Chip·감점 근거 Drawer·진단 미완료 경고 상태를 실제로 조립한다. 별도 `/reasons` Page는 만들지 않는다.
9. SCR-004 Owner는 구인 사이트 연결 Card Grid와 희망 직무 없음 Empty State를, SCR-005 Owner는 MBTI 16유형 그리드·태도 패널·미선택 상태·참고용 고지를 실제로 조립한다. 조립은 import만 하는 것이 아니라 화면 상태 전환까지 포함한다.
10. Page Owner AC에는 다음을 모두 기록한다(`audit_tasks.py`가 검사).
    - `Section 순서`와 D-001 §19의 Screen별 Section 이름, `Section별 데이터 출처`
    - 최소 콘텐츠 수: SCR-001 필수 필드 3·선택 필드 2, SCR-002 카테고리 4, SCR-003 추천 Card 6개, SCR-004 연결 Card 6개, SCR-005 유형 Card 16개
    - 반응형 콘텐츠 밀도(Desktop·Mobile)
    - `Empty State`(아이콘·제목·설명·다음 행동 CTA 포함), `Lorem ipsum`·`준비 중`·`정보 확인 필요` 금지, `빈 영역` 금지, `Preview` 확인

**데이터·API**
11. DB는 4개 테이블로 제한한다: `diagnosis_inputs`, `diagnosis_results`, `deduction_items`, `recommendation_items`(SRS §4.2). 스키마·접근 제어(RLS)·접근 함수는 별도 Task로 만든다.
12. 자격증·훈련 추천 매핑, 구인 사이트 검색 URL 템플릿, MBTI 16유형 매핑은 `src/data` 정적 데이터 `DATA` Task로 만든다. 외부 연동·크롤링·공고 매칭 Task는 만들지 않는다.
13. 구인 사이트 연결은 희망 직무 문자열을 검색 URL 템플릿에 치환하는 것까지만 한다. 공고 선별·정렬·추천·적합도 계산 Task는 만들지 않는다.
14. 희망 직무 값을 DB에 저장할지는 SRS `DiagnosisInput`에 필드가 없어 미결정(D-02)이다. 결정 전에는 DB 컬럼(`desired_job`)을 추가하는 Task를 만들지 않고, 결정 필요 사항은 `00_TASK_LIST.md`의 "가정과 블로킹 결정"에 기록한다.
15. MBTI 지표는 핵심 100점과 합산하는 로직·표시를 만들지 않는다.
16. 점수·감점·검증·링크 생성 순수 함수는 `LOGIC` Task로 만들고 단위 테스트 Task에 연결한다.

**범위 제한**
17. Playwright는 Chromium 핵심 흐름(5~7개)을 `E2E` Task 2~3개로 묶는다. Firefox·WebKit·부하 테스트 Task는 만들지 않는다.
18. 자동 Merge, EC2, AWS Task를 만들지 않는다. 허용되는 운영 Task는 CI(lint·typecheck·unit·build)와 Vercel 수동 배포·DB 연결 점검(`OPS`)뿐이다.
19. 로그인·관리자·결제·별점·광고 Task를 만들지 않는다. 관련 Requirement는 EXCLUDED다.

**Requirement 추적**
20. `PROJECT_SCOPE.md`의 모든 Requirement(현재 24개: REQ-FUNC 16, REQ-NFR 8)를 `00_TASK_LIST.md`의 "Requirement 추적표"에 IMPLEMENT 또는 EXCLUDED로 기록한다. PROJECT_SCOPE 상태와 다르게 적지 않는다.
21. IMPLEMENT Requirement는 구현 Task(Category가 TEST·E2E·MANUAL이 아닌 것)와 Test/Manual Check Task에 모두 연결한다. 브라우저 확인이 필요한 항목은 `MANUAL` Task 또는 `RELEASE-CHECK`에 연결한다.
22. EXCLUDED Requirement는 Task를 만들지 않으며 추적표에서 지우지 않고 "NON_IMPLEMENTATION" 표에 제외 근거와 후속 방향을 적는다.
23. 구현하지 않은 것을 구현했다고 기록하지 않는다. 모든 Task의 시작 상태는 미착수다.

**Task 목록**
24. Task ID는 의미 있는 대문자 ID(`PAGE-SCR001`, `DATA-JOBSITES`, `UNIT-SCORING` …)를 쓴다. Seq는 1부터 연속이다.
25. 코드 Task(`PAGE`, `COMPONENT`, `API`, `FOUNDATION`)의 Functional AC에는 "Next.js 구현 전 `node_modules/next/dist/docs/` 관련 문서 확인"을 넣는다(`AGENTS.md`: 이 Next.js 버전은 기존 지식과 다르다).
26. 시각 규칙은 D-001 Token만 쓴다. D-001에 없는 색·간격은 AC에서 요구하지 않는다.
27. 문서 상단 요약의 Task 수·Category별 수는 표와 일치해야 한다. Task 개수는 약 45~65개를 예상하되 개수를 완료 조건으로 쓰지 않는다. 한 Task는 하나의 검증 가능한 결과를 가진다.
28. 의사결정이 필요한 사항(채점 가중치 OQ-08, 감점 도출 OQ-13, 희망 직무 저장 D-02 등)은 임의로 확정하지 않고 "가정과 블로킹 결정"에 남긴다.

## Category

| Category | 용도 | 예 |
|---|---|---|
| `FOUNDATION` | 공통 기반 | 테스트 도구, Token CSS, 루트 Starter 제거, not-found, Header·Footer, Alert·Toast, 세션 Guard |
| `DATA` | `src/data` 정적 데이터 | 추천 매핑, 구인 사이트 URL 템플릿, MBTI 16유형 매핑 |
| `LOGIC` | 순수 함수 | 입력 검증, 점수 산출, 감점 근거, 추천 매핑, 링크 생성 |
| `DB` | 테이블·접근 | 4개 테이블 스키마, RLS, 접근 함수 |
| `API` | `src/app/api/**/route.ts`, 이벤트 기록 | API-01~04, 06, 07 |
| `COMPONENT` | 화면용 컴포넌트 | ScoreGauge, ReasonDrawer, RecommendationCard, MbtiGrid |
| `PAGE` | Page Entry 소유·조립 | Screen마다 1개 |
| `TEST` | 단위·접근 제어 테스트 | `UNIT-*`, `TEST-RLS-BASIC` |
| `E2E` | Playwright Chromium 핵심 흐름 | 2~3개 |
| `MANUAL` | 수동 확인·Release Check | 성능, Preview, 링크, 로그, `RELEASE-CHECK` |
| `OPS` | CI·배포 점검 | `OPS-CI`, `OPS-VERCEL-DB-CHECK` |

## 의존 순서 지침

`FOUNDATION`·`DB`·`DATA` → `LOGIC` → `API`·`COMPONENT` → `PAGE` → `TEST`·`E2E` → `MANUAL`·`OPS`. 기술 Route(`not-found`, `/` redirect)는 `FOUNDATION`으로 둔다.

## 00_TASK_LIST.md 형식

문서 구성: 제목·메타 → `## 0. 요약`(Task 총 N개, Category별 수, Requirement 수) → `## 1. 가정과 블로킹 결정` → `## 2. Task List` → `## 3. Screen ↔ Page Owner` → `## 4. Requirement 추적표` → `## 5. NON_IMPLEMENTATION` → `## 🔍 검증 체크`.

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
- Expected Files 값은 `` `create 경로` ``, `` `modify 경로` ``, `` `delete 경로` `` 형식이다.
- AC 셀의 여러 항목은 `1. … <br>2. …`로 구분한다. Implementation Status는 모두 `IMPLEMENT`다.
- Priority는 P0(Must·차단), P1(Should·검증), P2(보조)다.
- Requirement 추적표: `| Requirement | Status | 구현 Task | Test / Manual Check Task |`
- NON_IMPLEMENTATION: `| Requirement | 제외 근거 | 후속 방향 |`

## 상세 파일 TASKS/TASK-<Task ID>.md

`Implementation Status`가 IMPLEMENT인 모든 Task마다 정확히 하나를 만든다(EXCLUDED 행은 만들지 않음). 같은 ID 파일이 있으면 갱신하고 중복 파일을 만들지 않는다. `python scripts/gen_task_details.py`가 Task List에서 결정적으로 생성한다.

- 사전 검사: 중복 ID, 빈 필수 열, 존재하지 않는 Depends On이 있으면 파일을 만들지 않는다.
- 절(순서 고정, 14개): Context, Project Scope, Requirement Ref, Screen / Route / Page Entry, Design Ref, Depends On, Expected Files, Functional AC, Visual AC, Security/Privacy AC, Test Cases, Verify, Definition of Done, Forbidden
- 값(Requirement Ref·Depends On·Expected Files·Page Entry·AC 항목 수)은 Task List 행과 같아야 한다. 바꿔야 하면 `00_TASK_LIST.md`를 먼저 고치고 다시 생성한다.
- Expected Files 절에 "Expected Files 밖 수정 금지"를 기록한다. Page Owner는 Route Page 조립만 범위이며 하위 Component를 만들지 않는다(Expected Files는 Page Entry 하나).
- DB Task는 4개 테이블(`diagnosis_inputs`, `diagnosis_results`, `deduction_items`, `recommendation_items`)을 넘지 않는다.
- 생성 후 Task List 구현 ID와 파일명을 1:1 대조하고 `audit_tasks.py`를 실행한다. 실패하면 완료로 보고하지 않는다.

## 완료 조건

- `python scripts/validate_inputs.py` PASS
- `python scripts/audit_tasks.py` PASS(오류 0)
- Page Owner 5개, Route·Page Entry 중복 없음, Requirement 24개 전부 추적표에 기록
- 구현 Task ID와 `TASKS/TASK-*.md` 파일이 1:1
- 빠진 Requirement ID가 있으면 완료로 보고하지 않는다
- 감사 실패 시 보고만 하지 말고 Task 문서를 고쳐 다시 감사한다
