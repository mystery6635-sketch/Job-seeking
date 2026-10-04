# CLAUDE.md — JobFit (구직역량 진단 서비스) v1 MVP

이 파일은 이 저장소에서 작업할 때 지켜야 할 규칙을 모두 담는다. 다른 규칙 파일을 따로 읽지 않아도 작업을 시작할 수 있다.

## Harness Marker

```
HARNESS_SCHEMA=jobfit-screen-route-v1
DESIGN_PATH=design-reference/D-001/DESIGN.md
SCREEN_CONTRACT=design-reference/SCREEN_ROUTE_CONTRACT.json
PROJECT_SCOPE=docs/PROJECT_SCOPE.md
PLAYWRIGHT_ENABLED=true
PLAYWRIGHT_SCOPE=chromium-core-flows
AUTO_MERGE=false
AWS_ENABLED=false
```

`PLAYWRIGHT_SCOPE`는 Chromium 하나만 쓰고 Smoke 1개와 핵심 흐름 2개(E2E Task 3개)로 제한한다는 뜻이다(DEC-009).

## 프로젝트

AI 기반 구직역량 진단 서비스다. 구직자가 학력·나이·경력·자격증·skill·희망 직무를 입력하면 100점 만점 점수, 감점 근거, 자격증·훈련 추천, 외부 구인 사이트 검색 링크를 보여준다. MBTI 기반 직무 수행 태도는 100점과 합산하지 않는 참고용 보조 지표다.

- 스택: Next.js(App Router) + TypeScript(strict) + React + Tailwind CSS 4, DB는 Supabase(Postgres, DB 용도만), 테스트는 Vitest와 Playwright Chromium, 배포는 Vercel.
- 개발 루트는 이 폴더(`Job/app`)다. `backup_20261004/`는 복사본이므로 수정하지 않는다.
- 현재 코드는 create-next-app 스캐폴드뿐이다. 구현은 `TASKS/`의 Task로 진행한다. 구현하지 않은 것을 구현했다고 기록하지 않는다.
- 문서와 사용자 응답은 한국어로 쓴다. 코드 식별자는 영어를 쓴다.

## 정본 문서

| 대상 | 정본 |
|---|---|
| SRS | `docs/06_SRS_UIUX_REVISED.md` |
| Scope 분류(IMPLEMENT/EXCLUDED)와 확정된 결정 | `docs/PROJECT_SCOPE.md` (§6 채점 구간표·접근 제어·보존 SOP) |
| 디자인 | `design-reference/D-001/DESIGN.md` (LOCKED. 변경은 D-002를 새로 만든다) |
| Screen·Route·Page Entry | `design-reference/SCREEN_ROUTE_CONTRACT.json` |
| 화면별 영역·상태·금지 기능 | `design-reference/UI_CONTRACT.md` |
| Task | `TASKS/00_TASK_LIST.md`(목록 정본), `TASKS/TASK-<ID>.md`(상세) |
| 구조·결정 | `docs/ARCHITECTURE.md`, `docs/DECISION_LOG.md` |

서로 충돌하면 위 정본이 이긴다. `vendor/` 아래 파일은 참고용이며 구현 기준이 아니다.

## 화면(Screen)

| Screen | Route | Page Entry |
|---|---|---|
| SCR-001 진단 입력 (핵심) | `/diagnosis` | `src/app/diagnosis/page.tsx` |
| SCR-002 역량리포트 (핵심) | `/diagnosis/result` | `src/app/diagnosis/result/page.tsx` |
| SCR-003 직업훈련 추천 (핵심) | `/diagnosis/result/recommendations` | `src/app/diagnosis/result/recommendations/page.tsx` |
| SCR-004 직무추천 (핵심) | `/diagnosis/result/jobs` | `src/app/diagnosis/result/jobs/page.tsx` |
| SCR-005 직무수행태도 진단 (보조) | `/diagnosis/attitude` | `src/app/diagnosis/attitude/page.tsx` |

`/`(`src/app/page.tsx`)는 Screen이 아니라 `/diagnosis`로 redirect하는 기술 Route다. 감점 근거는 SCR-002 Drawer로 제공하며 `/diagnosis/result/reasons` Route를 만들지 않는다.

## 규칙

**시작 전**
1. 작업 전에 `package.json`과 `node_modules/next/dist/docs/`의 관련 문서를 확인한다. 이 Next.js 버전은 기존 지식과 API·규칙·파일 구조가 다를 수 있으므로 코드를 쓰기 전에 읽고 deprecation 안내를 따른다.
2. SRS 정본은 `docs/06_SRS_UIUX_REVISED.md`, Scope 분류 정본은 `docs/PROJECT_SCOPE.md`, 디자인 정본은 `design-reference/D-001/DESIGN.md`, Screen 정본은 `design-reference/SCREEN_ROUTE_CONTRACT.json`이다.
3. 시각 규칙은 D-001 Token만 쓴다. D-001에 없는 색·간격·그림자, 외부 서비스 상표·로고·고유 문구, 사이트 로고 이미지는 쓰지 않는다.

**Task 진행**
4. 개발 단위는 Task다. `/run-wave`는 `TASKS/WAVE_PLAN.md`가 있을 때만 쓴다(명령은 작성됐지만 Wave 구성은 아직 없음, DEC-010·011). 없으면 Task 단위로 진행한다. Wave 안에서도 Task는 `Depends On` 순서로 한 번에 하나만 구현한다.
5. 현재 Task의 `Expected Files` 밖 파일은 수정하지 않는다. 필요하면 먼저 `TASKS/00_TASK_LIST.md`를 고치고 `python scripts/gen_task_details.py`로 상세 파일을 다시 만든다.
6. Page Owner Task는 Page Entry에서 Component를 실제로 조립한다(import뿐 아니라 상태 전환까지). 하위 Component·API·Data 파일은 만들지 않는다.
7. SCR-001 Page Owner가 끝나면 create-next-app Starter 화면·문구가 남아 있지 않아야 한다(Starter 제거는 `FND-ROOT-REDIRECT`가 `src/app/page.tsx`에서 한다).
8. SCR-003은 추천 Card Grid와 감점 없음 Empty State를 상호 배타로 조립하고, 추천 Card는 6개 이상이다. 데이터가 없을 때도 아이콘·제목·설명·CTA가 있는 Empty State를 보여준다.
9. SCR-004는 구인 사이트 연결 Card 6개 이상과 희망 직무 없음 Empty State를, SCR-005는 MBTI 16유형 그리드·태도 패널·미선택 Empty State·"핵심 100점에 반영되지 않음" 고지를 조립한다. `Lorem ipsum`·`준비 중`·`정보 확인 필요` 문구와 큰 빈 영역은 금지다.
10. 한 Task가 여러 Page Entry를 소유하지 않는다.

**데이터·보안**
11. 진단 입력(학력·나이·경력·자격증·skill·희망 직무)은 `POST /api/diagnosis`로만 서버(DB)에 보낸다. URL 쿼리·콘솔 로그·분석 이벤트·외부 사이트로 보내지 않는다. 외부 구인 사이트에는 희망 직무 검색어만 URL에 담고, 이동·클릭 기록은 저장하지 않는다.
12. 브라우저에는 `result_id`만 `sessionStorage`에 보관한다. 이름·연락처·이력서 등 정의되지 않은 개인정보를 수집하지 않는다.
13. Supabase 쓰기는 진단 저장(`diagnosis_inputs`, `diagnosis_results`, `deduction_items`, `recommendation_items` 4개 테이블)으로 제한한다. 로그인·계정·관리자·결제 관련 테이블과 Auth는 만들지 않는다.
14. DB 접근은 서버(Route Handler)의 Supabase Server 클라이언트로만 한다. RLS를 우회하는 Client 코드, 브라우저 Supabase 클라이언트는 만들지 않는다. 4개 테이블에는 `anon`·`authenticated` 정책을 만들지 않는다.
15. Service Role Key는 Client에서 쓰지 않는다. 서버 전용 환경변수로만 두고 `NEXT_PUBLIC_` 접두어를 붙이지 않으며, `.env*` 파일과 키를 커밋하지 않는다.
16. 추천 매핑·구인 사이트 URL 템플릿·MBTI 매핑·채점 구간표는 `src/data`의 정적 TypeScript 데이터를 쓴다. 외부 연동·크롤링은 없다.
17. 점수는 `docs/PROJECT_SCOPE.md` §6.1 구간표(4개 카테고리 균등 25점)를 그대로 따르는 순수 함수로 계산한다. MBTI 지표를 100점에 합산하는 코드·표시는 만들지 않는다.

**범위 제한**
18. Prisma·ORM·AWS·EC2·CMS·외부 Email 공급자·정식 Monitoring을 추가하지 않는다. DB 스키마는 `db/migrations/*.sql`로 관리한다.
19. Playwright는 Chromium project 하나만 쓰고 Smoke 1개와 핵심 흐름 2개 외에는 작성하지 않는다. Firefox·WebKit·부하 테스트 없음. CI에는 lint·`tsc`·Vitest·build만 넣는다.
20. EXCLUDED 기능(`REQ-FUNC-PERSONALIZE-001~003`, `REQ-FUNC-ADMIN`, `REQ-NFR-AVAIL-001`, `REQ-NFR-PRIV-002`)과 로그인·결제·별점·광고·채용공고 매칭·추천 개인화를 임의로 구현하지 않는다.

**Git·진행**
21. destructive Git 명령(`reset --hard`, `clean -f`, `push --force`, `checkout -- .`, 브랜치 삭제 등)을 임의로 쓰지 않는다. 커밋·push는 사용자가 요청할 때만 한다.
22. 자동 PR·자동 Merge를 실행하지 않는다. PR·Merge는 사용자가 직접 한다.
23. 사람이 Desktop(1440)·Mobile(390) Preview를 확인하기 전에는 다음 Screen의 Page Owner로 넘어가지 않는다.
24. 작업을 마치면 변경 파일, 검증 결과(실행한 명령과 통과·실패), 남은 제한사항을 보고한다. 통과하지 못한 검증은 숨기지 않는다.

## Task 완료 순서

Task 읽기 → 입력 확인 → 구현 → 관련 포맷·Unit Test → 필요 시 Playwright → Diff 확인 → 완료 보고

- **Task 읽기**: `TASKS/TASK-<ID>.md`의 Depends On이 완료됐는지, Expected Files와 Forbidden을 확인한다.
- **입력 확인**: 관련 SRS 조항, UI_CONTRACT의 해당 Screen, D-001 해당 절, 현재 파일 트리(`create`/`modify` 대상이 맞는지)를 확인한다.
- **포맷·Unit Test**: `npm run lint`, 타입 검사, 해당 Vitest 테스트를 실행한다.
- **Playwright**: 해당 Task가 E2E일 때, 또는 화면 흐름이 바뀔 때만 Chromium으로 실행한다.
- **Diff 확인**: `git diff`로 Expected Files 밖 변경이 없는지 확인한다.

## 명령

| 용도 | 명령 |
|---|---|
| 개발 서버 | `npm run dev` |
| 린트 / 빌드 | `npm run lint` / `npm run build` |
| 입력 검증 | `python scripts/validate_inputs.py` (`VALIDATE_INPUTS_PASS`) |
| 상세 Task 생성 | `python scripts/gen_task_details.py` |
| Task 감사 | `python scripts/audit_tasks.py` (`AUDIT_PASS`, `TASKS/TASK_AUDIT_REPORT.md` 갱신) |
| 하네스 검증 | `python scripts/validate_harness.py` (`VALIDATE_HARNESS_PASS`) — CLAUDE.md·Skill·Command 규칙 확인 |

Vitest·Playwright 명령은 `FND-TEST-TOOLING` Task에서 `package.json`에 추가한다. 슬래시 명령은 `/gen-tasklist`, `/gen-task-details`, `/audit-tasks`, `/prepare-task <TASK_ID>`(구현 착수 전 읽기 전용 점검), `/implement-task <TASK_ID>`(점검 통과 Task 하나 구현), `/run-wave`(Wave 순차 실행, status·resume·dry-run 지원), `/release-check`(출시 점검, RELEASE_READY/BLOCKED)이며 `.claude/commands/`에 있다.

## 착수 차단

DB 관련 Task는 `.env.local`의 Supabase 접속 정보(서버 전용)가 있어야 실제 호출·테스트를 할 수 있다. 없으면 임의 값을 만들지 말고 해당 Task가 막혔다고 보고한다. UI·로직 Task(`FND-*`, `LIB-*`, `DATA-*`, `CMP-*`, `PAGE-*`)는 DB 없이 진행할 수 있다.
