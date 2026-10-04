# TASK-PAGE-SCR002 역량리포트 페이지 조립(Page Owner)

- Task ID: PAGE-SCR002
- Seq: 37
- Category: PAGE
- Priority: P0
- Status: NOT_STARTED

## Context

역량리포트 페이지 조립(Page Owner). Route Page(Page Entry)를 조립한다. 하위 Component를 새로 만들지 않고 import·상태 전환·데이터 연결만 한다.

선행 Task: `FND-SHELL`, `FND-SECTIONS`, `FND-SESSION-GUARD`, `CMP-SCORE-HERO`, `CMP-DEDUCTION-CHIPS`, `CMP-REASON-DRAWER`, `API-DIAG-RESULT`, `API-DIAG-REASONS`, `FEAT-OBS-EVENTS`.

이 Task에 의존하는 Task: `E2E-PUBLIC-SMOKE`, `E2E-DIAG-FLOW`, `MANUAL-PREVIEW`, `OPS-VERCEL-DB-CHECK`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-DIAG-001: 학력·나이·경력·자격증·skill 입력을 받아 100점 만점 점수를 산출하는 결정적 채점 함수 구현
- REQ-FUNC-DIAG-003: 채점 로직을 순수 함수로 구현하여 동일 입력에 동일 점수를 보장
- REQ-FUNC-SCORE-001: 진단 완료 후 "근거 보기" 클릭 시 항목별 감점 사유를 최소 3개 이상 표시
- REQ-FUNC-SCORE-002: 만점 항목은 "감점 없음"으로 구분 표시
- REQ-FUNC-SCORE-003: 진단 미완료 상태에서 근거 화면 접근 시 "먼저 진단을 완료해주세요" 안내로 전환하고 접근 차단
- REQ-NFR-OBS-001: 무료 분석 도구로 진단 완료·근거 화면 도달 이벤트만 최소 기록(Dummy)
- 범위: Route Page 조립(import·상태 전환·데이터 연결)만. 하위 Component 생성은 범위가 아니다.

## Requirement Ref

- REQ-FUNC-DIAG-001 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-DIAG-003 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-SCORE-001 (IMPLEMENT) — SRS §4.3.2 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-SCORE-002 (IMPLEMENT) — SRS §4.3.2 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-SCORE-003 (IMPLEMENT) — SRS §4.3.2 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-NFR-OBS-001 (IMPLEMENT) — SRS §4.4.4 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: SCR-002
- Route: `/diagnosis/result`
- Page Entry: `src/app/diagnosis/result/page.tsx`

## Design Ref

- `design-reference/D-001/DESIGN.md` §16 Page Section 최대 폭, §17 Hero 높이, §18 Section별 위계, §19 화면별 Section 순서와 최소 콘텐츠 수, §20 완성형 Empty State · Placeholder 금지
- `design-reference/UI_CONTRACT.md` SCR-002
- `design-reference/SCREEN_ROUTE_CONTRACT.json` SCR-002 (route·page_entry)

## Depends On

- `FND-SHELL` — 공통 Header·Footer·Breadcrumb
- `FND-SECTIONS` — 공통 Section 컴포넌트(Intro·Hero·StepGuide·CtaBanner)
- `FND-SESSION-GUARD` — 진단 세션 저장소와 미완료 접근 Guard
- `CMP-SCORE-HERO` — 결과 Hero·게이지·입력값 요약
- `CMP-DEDUCTION-CHIPS` — 카테고리 Chip 목록
- `CMP-REASON-DRAWER` — 감점 근거 Drawer
- `API-DIAG-RESULT` — GET /api/diagnosis/[result_id] (API-02)
- `API-DIAG-REASONS` — GET /api/diagnosis/[result_id]/reasons (API-03)
- `FEAT-OBS-EVENTS` — KPI 이벤트 기록(진단 완료·근거 화면 도달)

## Expected Files

- create: src/app/diagnosis/result/page.tsx
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. Next.js 구현 전 `node_modules/next/dist/docs/` 관련 문서 확인(AGENTS.md)
2. `/diagnosis/result`에서 Section 순서: 결과 Hero(100점 만점 총점) → 좌우 분할(게이지+입력값 요약) → 감점 근거 진입 CTA → 카테고리 Chip 목록 → (Drawer: 감점 근거) → 추천 이동 CTA Banner → 재진단 안내
3. Section별 데이터 출처: Hero·게이지·요약은 API-02, Chip·Drawer는 API-03, CTA는 정적 카피
4. 최소 콘텐츠: 카테고리 4개, 감점 사유 문장 총 4개(감점 없음 포함)
5. 진단 미완료 접근 시 `DiagnosisGuard`의 WarningAlert+SCR-001 CTA를 보여주고 결과를 렌더링하지 않는다. 로딩 Skeleton, 로드 실패 `error` Alert+`다시 시도`를 제공한다
6. `추천 확인하기`→SCR-003, `희망 직무로 구인 사이트 찾기`→SCR-004, `다시 진단하기`→SCR-001 이동을 연결한다

## Visual AC

1. Hero·좌우 분할·Chip 목록·CTA Banner의 형태가 교차하고 Desktop 5:7 분할, Mobile 게이지→요약 스택
2. Section 배경을 canvas↔surface-muted로 교대하고 같은 형태(Card Grid)를 연속 2개 Section에 배치하지 않는다
3. `Lorem ipsum`·`준비 중`·`정보 확인 필요`·`TBD`·`추후 제공`·내용 없는 Card·큰 빈 영역 금지. 데이터가 없는 경우에도 아이콘·제목·설명·CTA를 갖춘 Empty State를 표시한다

## Security/Privacy AC

1. 로그인·계정·관리자·결제·별점·광고 UI와 Route를 만들지 않는다

## Test Cases

- REQ-FUNC-DIAG-001: TC-DIAG-001-N
- REQ-FUNC-DIAG-003: TC-DIAG-003-N
- REQ-FUNC-SCORE-001: TC-SCORE-001-N
- REQ-FUNC-SCORE-002: TC-SCORE-002-N
- REQ-FUNC-SCORE-003: TC-SCORE-003-F
- REQ-NFR-OBS-001: TC-NFR-OBS-001-DRAFT
- SCR-002: AC-UI-03, 08, 09, 13~18 (`docs/05_UIUX_APPROVED.md` §6)

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
