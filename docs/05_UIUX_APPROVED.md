# UI/UX Approved — JobFit (SCR-001 ~ SCR-005)

| 항목 | 내용 |
|---|---|
| 문서 ID | UIUX-JOBFIT-001 |
| 기준일 | 2026-10-03 |
| Design Version | D-001 (LOCKED) — `design-reference/D-001/DESIGN.md` |
| 입력 문서 | `docs/02_SRS_BASELINE.md`, `docs/PROJECT_SCOPE.md`, `docs/03_UI_COVERAGE_ANALYSIS.md`, `design-reference/UI_CONTRACT.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json` |
| 후속 문서 | `docs/06_SRS_UIUX_REVISED.md`, `docs/UIUX_TRACEABILITY.md` |

---

## 1. 승인 Screen 목록

| Screen | 명칭 | 구분 | Route | Page Entry | Stitch 검증 |
|---|---|---|---|---|---|
| SCR-001 | 진단 입력 | 핵심 | `/diagnosis` | `src/app/diagnosis/page.tsx` | PASS |
| SCR-002 | 역량리포트 (진단 결과 + 감점 근거 Drawer) | 핵심 | `/diagnosis/result` | `src/app/diagnosis/result/page.tsx` | PASS |
| SCR-003 | 직업훈련 추천 | 핵심 | `/diagnosis/result/recommendations` | `src/app/diagnosis/result/recommendations/page.tsx` | PASS |
| SCR-004 | 직무추천 (외부 구인 사이트 검색 연결) | 핵심 | `/diagnosis/result/jobs` | `src/app/diagnosis/result/jobs/page.tsx` | NEEDS_REVISION (브레드크럼 문구) |
| SCR-005 | 직무수행태도 진단 (MBTI 참고용 보조 지표) | 보조 | `/diagnosis/attitude` | `src/app/diagnosis/attitude/page.tsx` | NEEDS_REVISION (브레드크럼 문구) |

- 핵심 4개는 진단 흐름(입력 → 결과 → 추천 → 직무 연결)이고, 보조 1개(SCR-005)는 진단 완료와 무관하게 접근하는 참고용 지표다.
- Screen은 5개로 고정한다. 기술 Route(`/` redirect, API Route, `not-found`)는 Screen 수에 포함하지 않는다.
- SCR-004·SCR-005의 Stitch 브레드크럼은 각각 "역량 리포트", "태도 진단"으로 남아 있어 탭 명칭과 불일치한다. Stitch 웹에서 수동 수정이 끝나기 전까지 두 화면의 시안 승인은 조건부이며, 구현은 탭 명칭("직무추천", "직무수행태도 진단")을 기준으로 한다.
- 시각 규칙은 D-001만 따른다. 디자인 Mobile 정본은 SCR-001, SCR-003이다.

## 2. 기존 Route → Screen 통합

SRS 기준 공개 Route 6개를 승인 Screen 5개로 통합한다.

| 기존 Route (SRS §3.6) | 통합 결과 | 통합 방식 |
|---|---|---|
| `/diagnosis` | SCR-001 | 단독 Screen |
| `/diagnosis/result` | SCR-002 | 단독 Screen |
| `/diagnosis/result/reasons` | SCR-002 | **Drawer(모바일 하단 시트)**로 통합. 별도 Route를 만들지 않으며 라우트 이동 없이 열린다 |
| `/diagnosis/result/recommendations` | SCR-003 | 단독 Screen |
| `/diagnosis/result/jobs` | SCR-004 | 단독 Screen |
| `/diagnosis/attitude` | SCR-005 | 단독 Screen |

기술 Route(Screen 아님)

| Route | 용도 | 비고 |
|---|---|---|
| `/` | `/diagnosis`로 redirect | 현재 `src/app/page.tsx`는 create-next-app 스타터이며 교체 대상 |
| `/api/diagnosis` | API-01 진단 제출 | POST |
| `/api/diagnosis/[result_id]` | API-02 결과 재조회 | GET |
| `/api/diagnosis/[result_id]/reasons` | API-03 감점 근거 데이터 | GET, SCR-002 Drawer가 사용 |
| `/api/diagnosis/[result_id]/recommendations` | API-04 추천 리스트 | GET |
| `/api/diagnosis/[result_id]/jobs` | API-06 구인 사이트 링크 목록 | GET |
| `/api/attitude` | API-07 MBTI 보조 지표 | GET |
| `not-found` | 존재하지 않는 경로 안내 | `/diagnosis` 이동 CTA 포함 |

## 3. Screen별 패널·모달 구성

| Screen | 패널/모달 | 연결 Requirement |
|---|---|---|
| SCR-001 | 필수 정보 Form, 선택 정보 Form(Chip 입력·"없음" 체크), 진단 3단계 안내, 제출 CTA Banner | REQ-FUNC-DIAG-001·002·004, REQ-NFR-PRIV-001 |
| SCR-002 | 결과 Hero, 게이지·입력값 요약, 카테고리 Chip 목록, **감점 근거 Drawer**, 진단 미완료 경고 Alert | REQ-FUNC-DIAG-001·003, REQ-FUNC-SCORE-001·002·003 |
| SCR-003 | 추천 Card Grid, 만점 Empty State, 활용 3단계 안내, 진단 미완료 경고 Alert | REQ-FUNC-RECO-001, REQ-FUNC-SCORE-003 |
| SCR-004 | 희망 직무 표시 바, 구인 사이트 연결 Card Grid, 희망 직무 없음 Empty State, 진단 미완료 경고 Alert | REQ-FUNC-JOBLINK-001·002, REQ-FUNC-SCORE-003 |
| SCR-005 | 참고용 고지 배너, MBTI 16유형 그리드, 태도 점수·강점·유의점 패널, 미선택 안내 상태 | REQ-FUNC-ATTITUDE-001·002 |

## 4. 제외 기능 (EXCLUDED)

화면·Route·컴포넌트를 만들지 않는다. 요구사항 ID와 명세는 SRS에 보존한다.

| 항목 | 상태 | 사유 |
|---|---|---|
| REQ-FUNC-PERSONALIZE-001~003 (추천 개인화) | EXCLUDED | Post-MVP 이연. PRD §10-2가 게이트 미통과 예외 편입임을 명시 |
| REQ-FUNC-ADMIN (관리자 기능) | EXCLUDED | 관리자·운영자 전용 화면은 PRD 근거 없음(OS-07, OQ-01) |
| REQ-NFR-AVAIL-001 (가동률 95%) | EXCLUDED | 측정 도구·정책 미정(OQ-15). 무료 업타임 도구 육안 확인만 수행 |
| REQ-NFR-PRIV-002 (보존기간 자동 삭제) | EXCLUDED | 보존기간 미정(OQ-20). 운영자 수동 삭제로 대체 |
| 로그인·인증·계정·프로필·내 활동 | EXCLUDED | OS-06, CON-07. v1은 계정 엔터티를 만들지 않음 |
| 유료 전환·결제·구독 | EXCLUDED | OS-02, CON-03 |
| 채용공고 매칭·추천·실시간 공고 feed | EXCLUDED | OS-03. SCR-004는 검색 URL 연결만 제공 |
| 커뮤니티·스터디, 사회적 Job 기능 | EXCLUDED | OS-04, OS-05 |
| 별점·리뷰·광고·통계 Dashboard | EXCLUDED | D-001 금지 규정 |

## 5. UI Route Contract

- 계약의 단일 출처는 `design-reference/SCREEN_ROUTE_CONTRACT.json`(`jobfit-screen-route-v1`, `nextjs-app-router`)이다.
- Screen은 정확히 5개이며 Route 5개와 Page Entry 5개는 서로 중복되지 않는다.
- 모든 Screen은 Page Owner Task와 Preview 확인이 필요하다. SCR-001은 스타터 템플릿 사용이 금지된다.
- 필수 이동 관계

| From | To | 트리거 | 유형 |
|---|---|---|---|
| SCR-001 | SCR-002 | 진단하기 제출 성공 | Route |
| SCR-002 | SCR-002 | 근거 보기 | Drawer |
| SCR-002 | SCR-003 | 추천 확인하기 | Route |
| SCR-002 | SCR-004 | 희망 직무로 구인 사이트 찾기 | Route |
| SCR-002 | SCR-001 | 다른 정보로 다시 진단하기 | Route |
| SCR-003 | SCR-002 / SCR-001 | 결과로 돌아가기 / 다시 진단하기 | Route |
| SCR-004 | SCR-002 / SCR-001 | 진단 결과로 돌아가기 / 다시 진단하기 | Route |
| SCR-004 | 외부 구인 사이트 | 희망 직무로 검색하기 | 새 탭 |
| SCR-005 | SCR-001 | 핵심 역량 진단 시작하기 | Route |
| SCR-002·003·004 | SCR-001 | 진단 미완료 경고 CTA | Route |
| Header | SCR-001 ~ SCR-005 | 탭 5개 | Route |

## 6. Release Acceptance Criteria (UI)

아래 항목을 모두 확인해야 UI 릴리스로 인정한다. 확인 전까지 체크하지 않는다.

**구조**
- [ ] AC-UI-01 Screen 5개가 Route Contract의 Route·Page Entry로 존재하고 Page Entry 파일이 5개 모두 다르다
- [ ] AC-UI-02 `src/app/page.tsx`가 스타터 화면이 아니며 `/diagnosis`로 redirect한다
- [ ] AC-UI-03 `/diagnosis/result/reasons` Page가 존재하지 않고 감점 근거는 SCR-002 Drawer로만 열린다
- [ ] AC-UI-04 Header 탭 5개와 Breadcrumb 2번째 구간이 모든 Screen에서 글자 단위로 일치한다
- [ ] AC-UI-05 로그인·관리자·결제·별점·광고 UI와 해당 Route가 존재하지 않는다

**기능·상태**
- [ ] AC-UI-06 SCR-001에서 필수 항목 누락 시 누락 항목을 명시한 오류가 표시되고 점수가 산출되지 않는다
- [ ] AC-UI-07 제출 중 "진단하기" 버튼이 비활성화되어 추가 요청이 발생하지 않는다
- [ ] AC-UI-08 SCR-002 Drawer가 감점 사유 3개 이상을 표시하고 만점 항목은 "감점 없음"으로 표시한다
- [ ] AC-UI-09 SCR-002·003·004를 진단 없이 열면 경고 안내와 SCR-001 이동 CTA가 표시된다
- [ ] AC-UI-10 SCR-003은 감점 항목이 있으면 추천 Card 6개 이상, 만점이면 Empty State를 표시하며 두 상태가 동시에 보이지 않는다
- [ ] AC-UI-11 SCR-004는 희망 직무가 있으면 연결 Card 6개 이상을 표시하고 각 링크가 새 탭으로 열린다. 없으면 Empty State만 표시한다
- [ ] AC-UI-12 SCR-005는 MBTI 미선택 시 안내와 선택 그리드만, 선택 후에는 점수·강점·유의점과 "핵심 역량 점수에 반영되지 않습니다" 고지를 표시한다
- [ ] AC-UI-13 어떤 화면에서도 MBTI 점수와 핵심 100점이 합산되거나 같은 시각 스타일로 표시되지 않는다

**디자인·접근성**
- [ ] AC-UI-14 사용 색상이 모두 D-001 Color Token에 속한다
- [ ] AC-UI-15 Desktop 1440px에서 Hero 아래 다음 Section이 첫 화면에 보이고, Mobile 390px에서 가로 스크롤이 없다
- [ ] AC-UI-16 Lorem ipsum, "준비 중", "정보 확인 필요" 등 D-001 §20 금지 문구와 빈 Card가 없다
- [ ] AC-UI-17 모든 인터랙티브 요소가 키보드로 조작되고 포커스 링이 보이며 터치 영역이 44px 이상이다. Drawer는 포커스 이동·Esc 닫기·복귀를 지원한다

**검증 증거**
- [ ] AC-UI-18 5개 Screen 각각 Desktop Preview, SCR-001·SCR-003은 Mobile Preview까지 확인한다
- [ ] AC-UI-19 SRS MVP Release Criteria(`docs/06_SRS_UIUX_REVISED.md` §9)와 Release Blocking OQ(OQ-08, 13, 16, 20) 결정 상태를 함께 확인한다

## 7. 현재 구현 현황

- `src/app`에는 `layout.tsx`, `page.tsx`, `globals.css`, `favicon.ico`만 있고 `page.tsx`는 create-next-app 스타터 그대로다.
- 5개 Screen Page, API Route, 공통 컴포넌트, `src/data` 정적 매핑, 테스트는 아직 구현되지 않았다. 모든 IMPLEMENT 요구사항의 Implementation Status는 `NOT_IMPLEMENTED`다.

## 8. 문서 간 불일치 기록

| 위치 | 불일치 | 처리 |
|---|---|---|
| `docs/PROJECT_SCOPE.md` §1 항목 1 | "핵심 화면 3개(`/diagnosis`, `/diagnosis/result`, `/diagnosis/result/reasons`) + 보조 화면 1개"로 적혀 있어 5개 Screen·reasons Drawer 통합과 다름 | 본 문서 §1·§2를 기준으로 한다. PROJECT_SCOPE 개정은 별도 작업 |
| `docs/03_UI_COVERAGE_ANALYSIS.md`, `docs/04_UIUX_PLAN.md` | Screen 명칭이 "진단 결과", "추천 리스트"이고 `04`는 포인트 컬러를 코랄로 기재 | 명칭은 D-001·Stitch 기준("역량리포트", "직업훈련 추천" 등)으로 통일. 색상은 D-001(Trust Blue)을 따른다 |
| `design-reference/DESIGN_MANIFEST.md` | `vendor/airbnb/DESIGN.md`가 저장소에 없음 | 별도 결정 필요 |
