# ARCHITECTURE — JobFit (구직역량 진단 서비스) v1 MVP

**작성일**: 2026-10-04
**근거**: `package.json`, `docs/06_SRS_UIUX_REVISED.md`, `docs/PROJECT_SCOPE.md`(§6 확정된 결정 포함), `design-reference/D-001/DESIGN.md`, `design-reference/UI_CONTRACT.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`, `TASKS/TASK_MANIFEST.csv`
**상태**: 구현 경계를 정하는 설계 문서다. 현재 코드는 create-next-app 스캐폴드뿐이며(`src/app`에 `layout.tsx`·`page.tsx`·`globals.css`), 아래 구조는 모두 `TASKS/`의 Task로 구현할 대상이다. 구현됐다는 뜻이 아니다.

## 1. 기술 스택

| 영역 | 선택 | 근거·비고 |
|---|---|---|
| 프레임워크 | Next.js 16.3.5, App Router | `package.json`. 이 버전은 기존 지식과 다르므로 구현 전 `node_modules/next/dist/docs/`를 확인한다(`AGENTS.md`) |
| 언어 | TypeScript 5 (`strict: true`) | `tsconfig.json` |
| UI | React 19.2.8, Tailwind CSS 4 | 시각 규칙은 D-001 Token만 사용 |
| DB | Supabase(Postgres) — **DB 용도만** | 결정 D-04. 인증·로그인 기능은 쓰지 않는다 |
| DB 접근 | `@supabase/supabase-js` 서버 클라이언트 | Prisma·ORM 미사용. 스키마는 `db/migrations/*.sql` |
| 단위 테스트 | Vitest | `FND-TEST-TOOLING`에서 설정 |
| E2E | Playwright, **Chromium 하나만** | Smoke 1개 + 핵심 흐름 2개(총 3 Task). Firefox·WebKit·부하 테스트 없음 |
| CI | GitHub Actions | lint·`tsc`·Vitest·build (`OPS-CI`). Playwright E2E는 CI에 넣지 않는다 |
| 배포 | Vercel | PR마다 Preview로 화면 확인, Production은 수동 배포 점검(`OPS-VERCEL-DB-CHECK`) |

현재 `package.json`에는 Vitest·Playwright·Supabase 클라이언트가 없다. 해당 Task에서 추가한다.

## 2. 화면과 Page Entry

핵심 4개와 보조 1개이며, 정본은 `SCREEN_ROUTE_CONTRACT.json`이다.

| Screen | 구분 | Route | Page Entry | Page Owner Task |
|---|---|---|---|---|
| SCR-001 진단 입력 | 핵심 | `/diagnosis` | `src/app/diagnosis/page.tsx` | `PAGE-SCR001` |
| SCR-002 역량리포트 | 핵심 | `/diagnosis/result` | `src/app/diagnosis/result/page.tsx` | `PAGE-SCR002` |
| SCR-003 직업훈련 추천 | 핵심 | `/diagnosis/result/recommendations` | `src/app/diagnosis/result/recommendations/page.tsx` | `PAGE-SCR003` |
| SCR-004 직무추천(외부 구인 사이트 연결) | 핵심 | `/diagnosis/result/jobs` | `src/app/diagnosis/result/jobs/page.tsx` | `PAGE-SCR004` |
| SCR-005 직무수행태도 진단(MBTI 보조 지표) | 보조 | `/diagnosis/attitude` | `src/app/diagnosis/attitude/page.tsx` | `PAGE-SCR005` |

- `/`(`src/app/page.tsx`)는 Screen이 아니라 `/diagnosis`로 redirect하는 기술 Route다(`FND-ROOT-REDIRECT`). 존재하지 않는 경로는 `src/app/not-found.tsx`가 안내한다.
- 감점 근거는 별도 Route 없이 SCR-002의 Drawer로 제공한다. `/diagnosis/result/reasons`는 만들지 않는다.
- 진단 흐름: SCR-001 → SCR-002 → SCR-003·SCR-004. SCR-005는 진단 완료와 무관하게 접근할 수 있고 핵심 100점과 합산하지 않는다.
- 한 Task는 하나의 Page Entry만 소유한다. Page Owner는 Route Page 조립만 하고 하위 Component를 만들지 않는다.

## 3. Server Component와 Client Component

원칙: `page.tsx`와 정적 Section은 Server Component로 두고, 브라우저 상태·이벤트·`sessionStorage`가 필요한 부분만 `'use client'`로 분리한다. 진단 결과는 `sessionStorage`의 `result_id`로 식별되므로 서버가 어떤 결과를 보여줄지 알 수 없다. 그래서 결과를 보여주는 Section은 Client Component(섬)이 `result_id`로 API를 호출해 채운다.

| 구분 | 대상 |
|---|---|
| Server Component | 5개 `page.tsx`, `layout.tsx`, `not-found.tsx`, `SiteFooter`, `PageIntro`, `Hero`, `StepGuide`, `CtaBanner`, `SectionBlock`, 정적 Alert·NoticeBanner·EmptyState |
| Client Component | `SiteHeader`(활성 탭·모바일 메뉴), `DiagnosisForm`와 입력 필드(Chip 입력·제출 상태), `DiagnosisGuard`(`sessionStorage`·미완료 접근 경고), `ScoreHero`·`InputSummary`, `ReasonDrawer`(포커스 트랩·Esc), `RecommendationGrid`, `JobSiteGrid`, `MbtiGrid`·`AttitudePanel`, `Toast`, 이벤트 기록(`analytics`) |

- Client Component는 데이터를 직접 DB에서 읽지 않는다. 항상 Route Handler(API)를 통한다.
- 점수·감점·추천·링크 생성 같은 순수 함수는 `src/lib/diagnosis/`에 두고 서버(API)에서 호출한다. 단위 테스트 대상이다.

## 4. 데이터 경계

### 4.1 정적 데이터 (`src/data`)

| 파일 | 내용 | Task |
|---|---|---|
| `src/data/recommendations.ts` | 자격증·훈련 추천 정적 매핑(카테고리 4개, 8개 이상) | `DATA-RECOMMENDATIONS` |
| `src/data/job-sites.ts` | 외부 구인 사이트 6곳의 검색 URL 템플릿 | `DATA-JOBSITES` |
| `src/data/mbti-attitude.ts` | MBTI 16유형 → 태도 점수·강점·유의점 | `DATA-MBTI-ATTITUDE` |
| `src/data/scoring-rules.ts` | 채점 구간표(`PROJECT_SCOPE.md` §6.1) | `LIB-SCORING-ENGINE` |

외부 데이터 연동·크롤링·DB 저장 없이 코드에 하드코딩한다. 추천·직무 사이트·MBTI는 DB에 넣을 시드가 없다(`DB-SEED-BASE`를 만들지 않는 결정 D-05).

### 4.2 DB — 4개 테이블

`diagnosis_inputs`, `diagnosis_results`, `deduction_items`, `recommendation_items`. 이 밖의 테이블은 만들지 않는다(계정·결제·관리자 테이블 포함).

- 희망 직무는 `diagnosis_inputs.desired_job` 선택 컬럼에 저장한다(결정 D-02).
- `result_id`는 추측할 수 없는 UUID이며 "해당 세션" 접근 제어의 열쇠다.
- 진단 입력·결과 보존기간은 90일이고 경과분은 운영자가 수동 삭제한다(자동 삭제 없음, `PROJECT_SCOPE.md` §6.3).

### 4.3 입력값이 가는 곳과 가지 않는 곳

| 입력 | 서버 API → DB | URL 쿼리 | 로그 | 분석 이벤트 | 외부 사이트 |
|---|---|---|---|---|---|
| 학력·나이·경력·자격증·skill | 저장(`POST /api/diagnosis`만) | 사용 안 함 | 원문 출력 금지 | 포함 안 함 | 보내지 않음 |
| 희망 직무 | 저장 | 사용 안 함 | 원문 출력 금지 | 포함 안 함 | **검색어로만** 구인 사이트 URL에 포함 |
| `result_id` | 저장·조회 키 | 사용 안 함 | 출력 금지 | 포함 안 함 | 보내지 않음 |
| MBTI 선택 | 저장 안 함(조회만) | 사용 안 함 | — | 포함 안 함 | 보내지 않음 |

- 외부 구인 사이트 이동은 새 탭 링크(`target="_blank"`, `rel="noopener noreferrer"`)일 뿐이며 이동·클릭 기록을 서버·DB에 저장하지 않는다.
- 브라우저에는 `result_id`만 `sessionStorage`에 보관한다(계정·인증 쿠키 없음, 가정 A-01).
- KPI 이벤트는 `diagnosis_completed`, `reasons_viewed` 두 개만 기록하며 payload에 입력값·점수·`result_id`를 넣지 않는다.

## 5. API (Route Handler)

| API | Route | Page Entry가 아닌 Route 파일 |
|---|---|---|
| API-01 | `POST /api/diagnosis` | `src/app/api/diagnosis/route.ts` |
| API-02 | `GET /api/diagnosis/[result_id]` | `.../[result_id]/route.ts` |
| API-03 | `GET /api/diagnosis/[result_id]/reasons` | `.../reasons/route.ts` |
| API-04 | `GET /api/diagnosis/[result_id]/recommendations` | `.../recommendations/route.ts` |
| API-06 | `GET /api/diagnosis/[result_id]/jobs` | `.../jobs/route.ts` |
| API-07 | `GET /api/attitude?mbti=` | `src/app/api/attitude/route.ts` |

API-05(개인화 추천)는 Post-MVP라 만들지 않는다. 서버 측 멱등키는 없고 중복 제출 방지는 클라이언트 버튼 비활성화로 한정한다.

## 6. Supabase 클라이언트와 접근 제어

- **Server 클라이언트만 사용한다**(`src/lib/db/client.ts`, `server-only`). 서버 전용 service key로 Route Handler 안에서만 DB에 접근한다.
- **Browser 클라이언트는 만들지 않는다.** 브라우저가 DB에 직접 닿을 이유가 없고, 4개 테이블에 `anon`·`authenticated` 정책이 없어 접근해도 거부된다.
- Supabase Auth는 쓰지 않는다. 로그인·회원가입·관리자 화면과 `auth callback` Route는 v1 범위 밖이다.
- RLS 원칙(간단하게): 4개 테이블 모두 RLS 활성화, 공개 정책 없음, 서버 전용 service key로만 접근. 질의는 필요한 컬럼만 선택하고 `result_id` 단건 조회만 한다.
- 저장 암호화는 Supabase 기본 저장 암호화를 사용하고 커스텀 암호화 계층은 만들지 않는다. 접근 이력은 Vercel·Supabase 플랫폼 기본 로그로 대체한다.
- 서버 전용 키에는 `NEXT_PUBLIC_` 접두어를 붙이지 않는다. 키는 `.env.local`과 Vercel 환경변수에만 두고 저장소에 올리지 않는다(`.gitignore`가 `.env*`를 제외).
- ORM(Prisma 등)을 쓰지 않는다. 마이그레이션은 SQL 파일로 관리한다.

## 7. 테스트와 배포

| 항목 | 방법 |
|---|---|
| 단위 테스트 | Vitest: 점수 산출, 입력 검증, 감점·추천 매핑, 링크 생성, MBTI 매핑, DB 접근 제어 |
| E2E | Playwright Chromium: `E2E-PUBLIC-SMOKE`(5개 Route·redirect·not-found), `E2E-DIAG-FLOW`, `E2E-JOBS-ATTITUDE` |
| CI | GitHub Actions에서 lint·타입 검사·Vitest·build만 실행 |
| Preview | Vercel Preview로 PR 화면 확인. Desktop(1440)·Mobile(390) Preview 확인은 `MANUAL-PREVIEW` |
| Production | Vercel 수동 배포와 DB 연결 확인(`OPS-VERCEL-DB-CHECK`) |
| 감사 | `python scripts/audit_tasks.py`가 Task 문서 일관성을 검사(코드·테스트 통과를 뜻하지 않음) |

## 8. 프로젝트 범위에서 제외

- **AWS·EC2**: 사용하지 않는다. 호스팅은 Vercel, DB는 Supabase다.
- **자동 Merge**: 사용하지 않는다. 병합은 사람이 직접 한다.
- **CMS**: 사용하지 않는다. 콘텐츠는 `src/data`와 코드에 둔다.
- **외부 Email 공급자**: 사용하지 않는다. 메일 발송·인증 메일이 없다.
- **Monitoring**: 정식 모니터링·감사 로그 시스템·부하 테스트 인프라는 만들지 않는다. 가동률 측정(REQ-NFR-AVAIL-001)은 EXCLUDED이며 KPI는 Vercel Analytics 기본 이벤트 2개만 쓴다.
- 그 밖: 로그인·계정, 결제·유료 전환, 채용공고 매칭·추천·크롤링, 추천 개인화, 관리자 화면, 커뮤니티.

## 9. 착수 차단

실제로 지금 없는 파일·환경변수만 적는다. 일반 UI·로직 Task(`FND-*`, `LIB-*`, `DATA-*`, `CMP-*`, `PAGE-*`)는 아래 항목 없이 착수할 수 있다.

| 누락 | 막히는 Task | 해소 방법 |
|---|---|---|
| `.env.local`(없음)과 Supabase 프로젝트 접속 정보: `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`(서버 전용). 변수 이름은 `DB-RLS-BASE`가 만드는 `.env.example`에서 확정한다 | `DB-SCHEMA-BASE`(적용), `DB-RLS-BASE`, `DB-ACCESS`, `TEST-RLS-BASIC`, `API-DIAG-*`의 실제 호출, `OPS-VERCEL-DB-CHECK` | Supabase 프로젝트를 만들고 키를 `.env.local`과 Vercel 환경변수에 등록 |
| Vercel 프로젝트 연결과 GitHub 원격 저장소(현재 로컬 저장소만 있음) | `OPS-CI`, `OPS-VERCEL-DB-CHECK`, Preview 확인 | 원격 저장소 생성·Vercel 연결 |

그 외 입력 문서·설계 문서·`node_modules/next/dist/docs/`는 모두 있어 차단이 아니다. Vitest·Playwright·Supabase 클라이언트 패키지는 Task에서 설치하는 대상이라 차단이 아니다.
