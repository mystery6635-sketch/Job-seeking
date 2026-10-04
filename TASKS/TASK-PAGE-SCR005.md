# TASK-PAGE-SCR005 직무수행태도 진단(MBTI 보조 지표) 페이지 조립(Page Owner)

- Task ID: PAGE-SCR005
- Seq: 40
- Category: PAGE
- Priority: P1
- Status: NOT_STARTED

## Context

직무수행태도 진단(MBTI 보조 지표) 페이지 조립(Page Owner). Route Page(Page Entry)를 조립한다. 하위 Component를 새로 만들지 않고 import·상태 전환·데이터 연결만 한다.

선행 Task: `FND-SHELL`, `FND-SECTIONS`, `CMP-MBTI-GRID`, `CMP-ATTITUDE-PANEL`, `API-ATTITUDE`, `DATA-MBTI-ATTITUDE`.

이 Task에 의존하는 Task: `E2E-PUBLIC-SMOKE`, `E2E-JOBS-ATTITUDE`, `MANUAL-PREVIEW`, `OPS-VERCEL-DB-CHECK`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-ATTITUDE-001: MBTI 16유형별 직무 수행 태도 점수·강점·유의점 정적 매핑 조회, 핵심 점수와 분리 고지
- REQ-FUNC-ATTITUDE-002: MBTI 미선택 시 선택 유도 안내와 선택 UI 표시
- 범위: Route Page 조립(import·상태 전환·데이터 연결)만. 하위 Component 생성은 범위가 아니다.

## Requirement Ref

- REQ-FUNC-ATTITUDE-001 (IMPLEMENT) — SRS §4.3.3c (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-ATTITUDE-002 (IMPLEMENT) — SRS §4.3.3c (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: SCR-005
- Route: `/diagnosis/attitude`
- Page Entry: `src/app/diagnosis/attitude/page.tsx`

## Design Ref

- `design-reference/D-001/DESIGN.md` §16 Page Section 최대 폭, §17 Hero 높이, §18 Section별 위계, §19 화면별 Section 순서와 최소 콘텐츠 수, §20 완성형 Empty State · Placeholder 금지
- `design-reference/UI_CONTRACT.md` SCR-005
- `design-reference/SCREEN_ROUTE_CONTRACT.json` SCR-005 (route·page_entry)

## Depends On

- `FND-SHELL` — 공통 Header·Footer·Breadcrumb
- `FND-SECTIONS` — 공통 Section 컴포넌트(Intro·Hero·StepGuide·CtaBanner)
- `CMP-MBTI-GRID` — MBTI 16유형 선택 그리드
- `CMP-ATTITUDE-PANEL` — 태도 점수·강점·유의점 패널
- `API-ATTITUDE` — GET /api/attitude?mbti= (API-07)
- `DATA-MBTI-ATTITUDE` — MBTI 16유형 직무 수행 태도 정적 데이터

## Expected Files

- create: src/app/diagnosis/attitude/page.tsx
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. Next.js 구현 전 `node_modules/next/dist/docs/` 관련 문서 확인(AGENTS.md)
2. `/diagnosis/attitude`에서 Section 순서: Intro(참고용 보조 지표 `info` 고지) → MBTI 16유형 선택 그리드 → 태도 점수·강점·유의점(선택 후) 또는 MBTI 미선택 Empty State(그리드 동시 노출) → CTA Banner
3. Section별 데이터 출처: 그리드·패널은 `DATA-MBTI-ATTITUDE`(API-07), Intro·CTA는 정적 카피
4. 최소 콘텐츠: 유형 Card 16개, 강점 2개 이상, 유의점 1개 이상. 진단 완료 여부와 무관하게 접근 가능
5. `핵심 100점에 반영되지 않음` 고지를 Intro와 결과 Section 양쪽에 표시한다. 핵심 진단 시작 CTA→SCR-001

## Visual AC

1. Desktop 4×4 그리드·결과 좌우 분할, Mobile 2열·결과 스택
2. 보조 지표는 핵심 점수 스타일과 시각적으로 구분된다
3. Section 배경을 canvas↔surface-muted로 교대하고 같은 형태(Card Grid)를 연속 2개 Section에 배치하지 않는다
4. `Lorem ipsum`·`준비 중`·`정보 확인 필요`·`TBD`·`추후 제공`·내용 없는 Card·큰 빈 영역 금지. 데이터가 없는 경우에도 아이콘·제목·설명·CTA를 갖춘 Empty State를 표시한다

## Security/Privacy AC

1. 로그인·계정·관리자·결제·별점·광고 UI와 Route를 만들지 않는다

## Test Cases

- REQ-FUNC-ATTITUDE-001: TC-ATTITUDE-001-N
- REQ-FUNC-ATTITUDE-002: TC-ATTITUDE-002-F
- SCR-005: AC-UI-12, 13, 14~18 (`docs/05_UIUX_APPROVED.md` §6)

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
