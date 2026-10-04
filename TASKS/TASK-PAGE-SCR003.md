# TASK-PAGE-SCR003 직업훈련 추천 페이지 조립(Page Owner)

- Task ID: PAGE-SCR003
- Seq: 38
- Category: PAGE
- Priority: P0
- Status: NOT_STARTED

## Context

직업훈련 추천 페이지 조립(Page Owner). Route Page(Page Entry)를 조립한다. 하위 Component를 새로 만들지 않고 import·상태 전환·데이터 연결만 한다.

선행 Task: `FND-SHELL`, `FND-SECTIONS`, `FND-SESSION-GUARD`, `CMP-RECO-GRID`, `API-DIAG-RECOMMENDATIONS`, `DATA-RECOMMENDATIONS`.

이 Task에 의존하는 Task: `E2E-PUBLIC-SMOKE`, `E2E-JOBS-ATTITUDE`, `MANUAL-PREVIEW`, `OPS-VERCEL-DB-CHECK`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-RECO-001: `src/data` 하드코딩 정적 매핑 테이블로 감점 항목 기반 추천 리스트 제공, 감점 항목 없으면 대체 안내
- REQ-FUNC-SCORE-003: 진단 미완료 상태에서 근거 화면 접근 시 "먼저 진단을 완료해주세요" 안내로 전환하고 접근 차단
- 범위: Route Page 조립(import·상태 전환·데이터 연결)만. 하위 Component 생성은 범위가 아니다.

## Requirement Ref

- REQ-FUNC-RECO-001 (IMPLEMENT) — SRS §4.3.3 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-SCORE-003 (IMPLEMENT) — SRS §4.3.2 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: SCR-003
- Route: `/diagnosis/result/recommendations`
- Page Entry: `src/app/diagnosis/result/recommendations/page.tsx`

## Design Ref

- `design-reference/D-001/DESIGN.md` §16 Page Section 최대 폭, §17 Hero 높이, §18 Section별 위계, §19 화면별 Section 순서와 최소 콘텐츠 수, §20 완성형 Empty State · Placeholder 금지
- `design-reference/UI_CONTRACT.md` SCR-003
- `design-reference/SCREEN_ROUTE_CONTRACT.json` SCR-003 (route·page_entry)

## Depends On

- `FND-SHELL` — 공통 Header·Footer·Breadcrumb
- `FND-SECTIONS` — 공통 Section 컴포넌트(Intro·Hero·StepGuide·CtaBanner)
- `FND-SESSION-GUARD` — 진단 세션 저장소와 미완료 접근 Guard
- `CMP-RECO-GRID` — 추천 Card Grid
- `API-DIAG-RECOMMENDATIONS` — GET /api/diagnosis/[result_id]/recommendations (API-04)
- `DATA-RECOMMENDATIONS` — 자격증·훈련 추천 정적 데이터

## Expected Files

- create: src/app/diagnosis/result/recommendations/page.tsx
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. Next.js 구현 전 `node_modules/next/dist/docs/` 관련 문서 확인(AGENTS.md)
2. `/diagnosis/result/recommendations`에서 Section 순서: Intro → 추천 Card Grid(감점 있음) 또는 감점 없음 Empty State(상호 배타) → 활용 3단계 안내 → CTA Banner
3. Section별 데이터 출처: Grid는 API-04(`DATA-RECOMMENDATIONS`), 3단계·CTA는 정적 카피
4. 최소 콘텐츠: 추천 Card 6개 이상(미달 시 Grid 대신 완성형 Empty State), 3단계 3개
5. 진단 미완료 접근 시 WarningAlert+SCR-001 CTA, `결과로 돌아가기`→SCR-002, `다시 진단하기`→SCR-001

## Visual AC

1. Desktop 3열(20px 간격)·Mobile 1열(Mobile 정본 화면)
2. Intro→Grid 형태 교차 유지
3. Section 배경을 canvas↔surface-muted로 교대하고 같은 형태(Card Grid)를 연속 2개 Section에 배치하지 않는다
4. `Lorem ipsum`·`준비 중`·`정보 확인 필요`·`TBD`·`추후 제공`·내용 없는 Card·큰 빈 영역 금지. 데이터가 없는 경우에도 아이콘·제목·설명·CTA를 갖춘 Empty State를 표시한다

## Security/Privacy AC

1. 로그인·계정·관리자·결제·별점·광고 UI와 Route를 만들지 않는다

## Test Cases

- REQ-FUNC-RECO-001: TC-RECO-001-DRAFT
- REQ-FUNC-SCORE-003: TC-SCORE-003-F
- SCR-003: AC-UI-09, 10, 14~18 (`docs/05_UIUX_APPROVED.md` §6)

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
