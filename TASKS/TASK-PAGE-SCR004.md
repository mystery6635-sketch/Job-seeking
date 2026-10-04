# TASK-PAGE-SCR004 직무추천(외부 구인 사이트 검색 연결) 페이지 조립(Page Owner)

- Task ID: PAGE-SCR004
- Seq: 39
- Category: PAGE
- Priority: P0
- Status: NOT_STARTED

## Context

직무추천(외부 구인 사이트 검색 연결) 페이지 조립(Page Owner). Route Page(Page Entry)를 조립한다. 하위 Component를 새로 만들지 않고 import·상태 전환·데이터 연결만 한다.

선행 Task: `FND-SHELL`, `FND-SECTIONS`, `FND-SESSION-GUARD`, `CMP-JOB-SITES`, `API-DIAG-JOBS`, `DATA-JOBSITES`.

이 Task에 의존하는 Task: `E2E-PUBLIC-SMOKE`, `E2E-JOBS-ATTITUDE`, `MANUAL-PREVIEW`, `OPS-VERCEL-DB-CHECK`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-JOBLINK-001: 희망 직무 문자열을 사이트별 검색 URL 템플릿에 치환해 잡코리아·사람인·원티드·워크넷·IT 전문 구인 사이트 링크를 새 탭으로 연결(매칭·추천 로직 없음)
- REQ-FUNC-JOBLINK-002: 희망 직무 정보 없음 시 안내 문구와 재진단 CTA 표시
- REQ-FUNC-SCORE-003: 진단 미완료 상태에서 근거 화면 접근 시 "먼저 진단을 완료해주세요" 안내로 전환하고 접근 차단
- 범위: Route Page 조립(import·상태 전환·데이터 연결)만. 하위 Component 생성은 범위가 아니다.

## Requirement Ref

- REQ-FUNC-JOBLINK-001 (IMPLEMENT) — SRS §4.3.3b (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-JOBLINK-002 (IMPLEMENT) — SRS §4.3.3b (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-SCORE-003 (IMPLEMENT) — SRS §4.3.2 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: SCR-004
- Route: `/diagnosis/result/jobs`
- Page Entry: `src/app/diagnosis/result/jobs/page.tsx`

## Design Ref

- `design-reference/D-001/DESIGN.md` §16 Page Section 최대 폭, §17 Hero 높이, §18 Section별 위계, §19 화면별 Section 순서와 최소 콘텐츠 수, §20 완성형 Empty State · Placeholder 금지
- `design-reference/UI_CONTRACT.md` SCR-004
- `design-reference/SCREEN_ROUTE_CONTRACT.json` SCR-004 (route·page_entry)

## Depends On

- `FND-SHELL` — 공통 Header·Footer·Breadcrumb
- `FND-SECTIONS` — 공통 Section 컴포넌트(Intro·Hero·StepGuide·CtaBanner)
- `FND-SESSION-GUARD` — 진단 세션 저장소와 미완료 접근 Guard
- `CMP-JOB-SITES` — 구인 사이트 연결 Card Grid
- `API-DIAG-JOBS` — GET /api/diagnosis/[result_id]/jobs (API-06)
- `DATA-JOBSITES` — 외부 구인 사이트 검색 URL 템플릿 정적 데이터

## Expected Files

- create: src/app/diagnosis/result/jobs/page.tsx
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. Next.js 구현 전 `node_modules/next/dist/docs/` 관련 문서 확인(AGENTS.md)
2. `/diagnosis/result/jobs`에서 Section 순서: Intro(희망 직무 표시 바) → 구인 사이트 연결 Card Grid(희망 직무 있음) 또는 희망 직무 없음 Empty State(상호 배타) → CTA Banner
3. Section별 데이터 출처: Card는 API-06+`DATA-JOBSITES`, 희망 직무는 진단 세션, CTA는 정적 카피
4. 최소 콘텐츠: 연결 Card 6개 이상, 고지 문장 1개(`특정 공고를 선별·추천하지 않으며…`)
5. Breadcrumb 2번째 구간은 `직무추천`이다. 진단 미완료 접근 시 WarningAlert+SCR-001 CTA

## Visual AC

1. Desktop 3열·Mobile 1열, 고지 문장이 Grid 하단에 위치
2. Section 배경을 canvas↔surface-muted로 교대하고 같은 형태(Card Grid)를 연속 2개 Section에 배치하지 않는다
3. `Lorem ipsum`·`준비 중`·`정보 확인 필요`·`TBD`·`추후 제공`·내용 없는 Card·큰 빈 영역 금지. 데이터가 없는 경우에도 아이콘·제목·설명·CTA를 갖춘 Empty State를 표시한다

## Security/Privacy AC

1. 로그인·계정·관리자·결제·별점·광고 UI와 Route를 만들지 않는다

## Test Cases

- REQ-FUNC-JOBLINK-001: TC-JOBLINK-001-N
- REQ-FUNC-JOBLINK-002: TC-JOBLINK-002-F
- REQ-FUNC-SCORE-003: TC-SCORE-003-F
- SCR-004: AC-UI-09, 11, 14~18 (`docs/05_UIUX_APPROVED.md` §6)

## Verify

- `npm run lint`, `npm run build`, Desktop(1440)·Mobile(390) Preview 확인(MANUAL-PREVIEW)

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목을 모두 충족했다
- [ ] Verify의 명령·확인을 실행해 결과를 기록했다(통과하지 못하면 완료로 보고하지 않는다)
- [ ] Expected Files에 없는 파일을 수정하지 않았다
- [ ] Forbidden 항목에 해당하는 변경이 없다
- [ ] Desktop(1440)·Mobile(390) Preview에서 Section 순서·최소 콘텐츠 수·Empty State를 확인했다
- [ ] 구현 전 `node_modules/next/dist/docs/` 관련 문서를 확인했다

## Forbidden

- Expected Files 밖 파일 수정·생성 금지(필요하면 먼저 `TASKS/00_TASK_LIST.md`를 고친다)
- 로그인·계정·관리자·결제·별점·광고 UI·Route 추가 금지
- D-001 Token에 없는 색·간격·그림자 추가 금지
- `Lorem ipsum`·`준비 중`·`정보 확인 필요`·`TBD` 등 Placeholder 문구 금지
- 자동 Merge·EC2·AWS 설정 추가 금지
- 구현 코드·Branch·Commit을 이 문서 작업으로 만들지 않는다
- 하위 Component·API·Data 파일을 새로 만들거나 수정하지 않는다(Page 조립만)
- 다른 Screen의 Page Entry를 수정하지 않는다
