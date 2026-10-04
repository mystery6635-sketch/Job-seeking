# TASK-PAGE-SCR001 진단 입력 페이지 조립(Page Owner)

- Task ID: PAGE-SCR001
- Seq: 36
- Category: PAGE
- Priority: P0
- Status: NOT_STARTED

## Context

진단 입력 페이지 조립(Page Owner). Route Page(Page Entry)를 조립한다. 하위 Component를 새로 만들지 않고 import·상태 전환·데이터 연결만 한다.

선행 Task: `FND-SHELL`, `FND-SECTIONS`, `FND-ROOT-REDIRECT`, `CMP-FIELDS`, `CMP-DIAG-FORM`, `API-DIAG-SUBMIT`, `FEAT-OBS-EVENTS`.

이 Task에 의존하는 Task: `E2E-PUBLIC-SMOKE`, `E2E-DIAG-FLOW`, `MANUAL-PREVIEW`, `OPS-VERCEL-DB-CHECK`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-DIAG-001: 학력·나이·경력·자격증·skill 입력을 받아 100점 만점 점수를 산출하는 결정적 채점 함수 구현
- REQ-FUNC-DIAG-002: 필수 항목(학력·나이·경력) 누락 시 점수 산출 이전에 검증하여 누락 항목을 명시한 오류 메시지 표시
- REQ-FUNC-DIAG-004: 진단 제출 시작 시 "진단하기" 버튼 비활성화, 응답 수신 후 재활성화(클라이언트 수준)
- REQ-NFR-PRIV-001: 입력 폼을 진단에 필요한 항목(학력·나이·경력·자격증·skill)과 희망 직무로만 한정 설계
- REQ-NFR-PERF-001: 진단 요청 후 5초 이내 결과 반환을 목표로 채점 로직을 동기·경량 함수로 구현
- REQ-NFR-OBS-001: 무료 분석 도구로 진단 완료·근거 화면 도달 이벤트만 최소 기록(Dummy)
- 범위: Route Page 조립(import·상태 전환·데이터 연결)만. 하위 Component 생성은 범위가 아니다.

## Requirement Ref

- REQ-FUNC-DIAG-001 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-DIAG-002 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-DIAG-004 (IMPLEMENT) — SRS §4.3.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-NFR-PRIV-001 (IMPLEMENT) — SRS §4.4.3 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-NFR-PERF-001 (IMPLEMENT) — SRS §4.4.1 (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-NFR-OBS-001 (IMPLEMENT) — SRS §4.4.4 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: SCR-001
- Route: `/diagnosis`
- Page Entry: `src/app/diagnosis/page.tsx`

## Design Ref

- `design-reference/D-001/DESIGN.md` §16 Page Section 최대 폭, §17 Hero 높이, §18 Section별 위계, §19 화면별 Section 순서와 최소 콘텐츠 수, §20 완성형 Empty State · Placeholder 금지
- `design-reference/UI_CONTRACT.md` SCR-001
- `design-reference/SCREEN_ROUTE_CONTRACT.json` SCR-001 (route·page_entry)

## Depends On

- `FND-SHELL` — 공통 Header·Footer·Breadcrumb
- `FND-SECTIONS` — 공통 Section 컴포넌트(Intro·Hero·StepGuide·CtaBanner)
- `FND-ROOT-REDIRECT` — 루트 Starter 제거와 /diagnosis redirect
- `CMP-FIELDS` — 입력 필드 컴포넌트(TextField·SelectField·ChipInput·NoneCheckbox)
- `CMP-DIAG-FORM` — 진단 입력 Form 컴포넌트
- `API-DIAG-SUBMIT` — POST /api/diagnosis (API-01)
- `FEAT-OBS-EVENTS` — KPI 이벤트 기록(진단 완료·근거 화면 도달)

## Expected Files

- create: src/app/diagnosis/page.tsx
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. Next.js 구현 전 `node_modules/next/dist/docs/` 관련 문서 확인(AGENTS.md)
2. `/diagnosis`에서 Section 순서: Hero → 필수 정보 Form(학력·나이·경력) → 선택 정보 Form(자격증·skill·희망 직무) → 진단 3단계 안내 → 제출 CTA Banner
3. Section별 데이터 출처: Hero·3단계 안내·CTA는 컴포넌트 내 한국어 정적 카피, Form은 `DiagnosisForm`(API-01 호출)
4. 최소 콘텐츠: 필수 필드 3개, 선택 필드 2개+희망 직무, 안내 단계 3개. 이 화면은 목록 데이터가 없어 Empty State 대신 필드 오류·제출 실패 상태를 완성형(원인+해결 방법)으로 제공한다
5. `create-next-app` Starter 템플릿 사용 금지, `/diagnosis`는 5개 Screen 중 SCR-001만 이 Page Entry를 소유한다

## Visual AC

1. Desktop: Hero 360~480px 후 Form 상단이 첫 화면에 보이고 Form 1~2열. Mobile: 1열·제출 버튼 폭 100%·52px(Mobile 정본 화면)
2. 섹션 상하 여백 Desktop 80px·Mobile 48px
3. Section 배경을 canvas↔surface-muted로 교대하고 같은 형태(Card Grid)를 연속 2개 Section에 배치하지 않는다
4. `Lorem ipsum`·`준비 중`·`정보 확인 필요`·`TBD`·`추후 제공`·내용 없는 Card·큰 빈 영역 금지. 데이터가 없는 경우에도 아이콘·제목·설명·CTA를 갖춘 Empty State를 표시한다

## Security/Privacy AC

1. 로그인·계정·관리자·결제·별점·광고 UI와 Route를 만들지 않는다

## Test Cases

- REQ-FUNC-DIAG-001: TC-DIAG-001-N
- REQ-FUNC-DIAG-002: TC-DIAG-002-F
- REQ-FUNC-DIAG-004: TC-DIAG-004-N
- REQ-NFR-PRIV-001: TC-NFR-PRIV-001
- REQ-NFR-PERF-001: TC-NFR-PERF-001
- REQ-NFR-OBS-001: TC-NFR-OBS-001-DRAFT
- SCR-001: AC-UI-01, 02, 05, 06, 07, 14~18 (`docs/05_UIUX_APPROVED.md` §6)

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
