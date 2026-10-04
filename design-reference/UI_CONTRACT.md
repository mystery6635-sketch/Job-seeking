# UI Contract — JobFit (SCR-001 ~ SCR-005)

**근거**: `docs/03_UI_COVERAGE_ANALYSIS.md`, `docs/04_UIUX_PLAN.md`, `docs/STITCH_VALIDATION_REPORT.md`, `design-reference/D-001/DESIGN.md`
**기계 판독본**: `design-reference/SCREEN_ROUTE_CONTRACT.json` (Route·Page Entry·이동 관계의 단일 출처)
**Design Version**: D-001 (LOCKED) — 시각 규칙은 D-001만 따른다.

## 0. 공통 계약

| 구분 | Screen | 비고 |
|---|---|---|
| **핵심 4개** | SCR-001, SCR-002, SCR-003, SCR-004 | 진단 흐름(입력 → 결과 → 추천 → 직무 연결) |
| **보조 1개** | SCR-005 | MBTI 참고용 보조 지표. 진단 완료와 무관하게 접근 가능, 100점에 합산 금지 |

- 모든 Page는 `src/app/**/page.tsx` 에서 직접 소유(Page Owner Task 필수)하고, 구현 후 Preview 확인이 필수다.
- 공통 Header/Footer/Alert/Drawer 컴포넌트는 `src/components`에 두고 5개 화면이 공유한다. Header 탭 5개와 Breadcrumb 2번째 구간은 글자 단위로 동일해야 한다(D-001 §7).
- **현재 `src/app` 상태**: `page.tsx`, `layout.tsx`, `globals.css`만 있고 `page.tsx`는 create-next-app 스타터 그대로다. 5개 Screen 어느 Page도 아직 없다.
- `/`(루트)는 Screen이 아니다. `/diagnosis`로 redirect하는 기술 Route이며 스타터 화면을 남기지 않는다.
- 진단 결과는 세션 단위 `result_id`로 식별한다. SCR-002~004는 진단 미완료 접근 시 동일한 경고 패턴을 사용한다(D-001 §13).
- 모든 화면 공통 금지: 로그인·계정·관리자, 결제·구독·가격, 별점·리뷰·광고, 실시간 공고 feed, 통계 Dashboard, EXCLUDED 요구사항(PERSONALIZE-001~003, ADMIN, AVAIL-001, PRIV-002) 대응 UI.

---

## SCR-001 진단 입력 (핵심)

| 항목 | 내용 |
|---|---|
| Route | `/diagnosis` |
| Page Entry | `src/app/diagnosis/page.tsx` (`starter_template_forbidden`) |
| 영역 순서 | 1 Hero → 2 필수 정보 Form(학력·나이·경력) → 3 선택 정보 Form(자격증·skill, 희망 직무) → 4 진단 3단계 안내 → 5 제출 CTA Banner |
| 주요 Component | `SiteHeader`, `Hero`, `DiagnosisForm`, `TextField`/`SelectField`, `ChipInput`, `NoneCheckbox`, `StepGuide`, `CtaBanner`, `SiteFooter` |
| 상태 | 초기 입력 / 필수 누락 오류(필드 하단 `error` 메시지) / 제출 중(버튼 비활성 + 스피너) / 제출 실패(Alert + 다시 시도) / 제출 완료 → SCR-002 이동 |
| 사용자 행동 | 필수 3개 입력, 자격증·skill Chip 추가·삭제, "없음" 체크, 희망 직무 입력, "진단하기" 제출, Hero CTA로 폼까지 스크롤 |
| 이동 | 제출 성공 → SCR-002. Header 탭·"진단 시작하기" → 각 화면 |
| Desktop | 1200px 컨테이너, Hero 360~480px 후 Form 상단이 첫 화면에 보임, Form은 1~2열 |
| Mobile | 1열, 제출 버튼 폭 100%·52px, Mobile 정본 화면 |
| 금지 기능 | 회원가입·로그인 유도, 이력서 파일 업로드, 개인 식별 정보(이름·연락처) 수집, 결제, 진단 중복 제출 |

## SCR-002 역량리포트 (핵심)

| 항목 | 내용 |
|---|---|
| Route | `/diagnosis/result` |
| Page Entry | `src/app/diagnosis/result/page.tsx` |
| 영역 순서 | 1 결과 Hero(100점 만점 총점) → 2 좌우 분할(게이지 + 입력값 요약) → 3 감점 근거 진입 CTA → 4 카테고리 Chip 목록(학력/경력/자격증/스킬) → 5 추천 이동 CTA Banner → 6 재진단 안내 (Drawer: 감점 근거) |
| 주요 Component | `ScoreHero`, `ScoreGauge`, `InputSummary`, `DeductionChipList`, `ReasonDrawer`, `ReasonItemCard`, `CtaBanner`, `WarningAlert` |
| 상태 | 결과 로딩(Skeleton) / 결과 표시 / 진단 미완료 접근(`warning` Alert + SCR-001 CTA) / Drawer 열림·닫힘 / 로드 실패(`error` Alert + 다시 시도) |
| 사용자 행동 | 점수 확인, "근거 보기"로 Drawer 열기(Esc·Scrim으로 닫기), 감점 사유 열람(최소 3개, 만점 항목은 "감점 없음"), 추천 확인, 재진단 |
| 이동 | 근거 보기 → Drawer(라우트 변경 없음) / 추천 확인하기 → SCR-003 / 직무 연결 → SCR-004 / 다시 진단 → SCR-001 |
| Desktop | 좌우 분할 5:7, Drawer는 우측 480px 패널 |
| Mobile | 게이지 → 요약 순 스택, Drawer는 하단 시트(최대 90vh) |
| 금지 기능 | `/diagnosis/result/reasons` 별도 라우트, 동종 인원 대비 순위·백분위 비교, 점수 공유/결제 유도, 통계 차트, 100점에 MBTI 점수 합산 |

## SCR-003 직업훈련 추천 (핵심)

| 항목 | 내용 |
|---|---|
| Route | `/diagnosis/result/recommendations` |
| Page Entry | `src/app/diagnosis/result/recommendations/page.tsx` |
| 영역 순서 | 1 Intro → 2 추천 Card Grid(6개 이상) → 3 감점 없음 Empty State(만점 시, Grid와 상호 배타) → 4 활용 3단계 안내 → 5 CTA Banner |
| 주요 Component | `PageIntro`, `RecommendationCard`, `RecommendationGrid`, `EmptyState`, `StepGuide`, `CtaBanner`, `WarningAlert` |
| 상태 | 목록 로딩 / 추천 표시(정적 매핑) / 만점 Empty State / 진단 미완료 접근 경고 / 로드 실패 |
| 사용자 행동 | 감점 항목별 추천 확인, Card의 자세히 알아보기, 결과로 돌아가기, 다시 진단 |
| 이동 | 결과로 돌아가기 → SCR-002 / 다시 진단하기 → SCR-001 |
| Desktop | Card 3열(20px 간격), Intro→Grid 형태 교차 유지 |
| Mobile | Card 1열, Mobile 정본 화면 |
| 금지 기능 | 과정 신청·결제·수강 등록, 가격·별점·후기, 개인화·학습이력 기반 추천(Post-MVP), 광고 Card |

## SCR-004 직무추천 — 외부 구인 사이트 검색 연결 (핵심)

| 항목 | 내용 |
|---|---|
| Route | `/diagnosis/result/jobs` |
| Page Entry | `src/app/diagnosis/result/jobs/page.tsx` |
| 영역 순서 | 1 Intro(+희망 직무 표시 바) → 2 구인 사이트 연결 Card Grid(6개 이상: 잡코리아·사람인·원티드·워크넷·프로그래머스 잡·로켓펀치) → 3 희망 직무 없음 Empty State(Grid와 상호 배타) → 4 CTA Banner |
| 주요 Component | `PageIntro`, `JobQueryBar`, `JobSiteCard`, `EmptyState`, `NoticeBanner`(info), `CtaBanner`, `WarningAlert` |
| 상태 | 연결 Card 로딩 / Card 표시 / 희망 직무 없음 Empty State / 진단 미완료 접근 경고 |
| 사용자 행동 | 사이트별 "희망 직무로 검색하기"(새 탭), 결과·재진단으로 이동 |
| 이동 | Card → 외부 사이트 새 탭(`rel="noopener noreferrer"`) / 진단 결과로 돌아가기 → SCR-002 / 다시 진단하기 → SCR-001 |
| Desktop | Card 3열, 고지 문장 Grid 하단 |
| Mobile | Card 1열 |
| 금지 기능 | 공고 매칭·추천·랭킹, 실시간 공고 feed·크롤링, 사이트 로고 이미지, 지원·이력서 제출, 광고. 고지 필수: "특정 공고를 선별·추천하지 않으며 희망 직무는 검색창 채움 용도로만 사용됩니다" |
| 보류 | Stitch 브레드크럼이 "역량 리포트"로 남아 있음 → "직무추천"으로 수동 수정 필요(코드 구현은 "직무추천" 기준) |

## SCR-005 직무수행태도 진단 — MBTI 보조 지표 (보조)

| 항목 | 내용 |
|---|---|
| Route | `/diagnosis/attitude` |
| Page Entry | `src/app/diagnosis/attitude/page.tsx` |
| 영역 순서 | 1 Intro(참고용 보조 지표 고지, `info`) → 2 MBTI 16유형 선택 그리드 → 3 태도 점수·강점·유의점(선택 후 노출) → 4 CTA Banner |
| 주요 Component | `PageIntro`, `NoticeBanner`(info), `MbtiGrid`, `MbtiTypeCard`, `AttitudePanel`, `AuxiliaryBadge`, `CtaBanner` |
| 상태 | MBTI 미선택(그리드 + 안내만, 결과 숨김) / 선택 완료(결과 표시) / 로드 실패. 진단 완료 전제 없음 |
| 사용자 행동 | 16유형 중 1개 선택(방향키 이동), 다른 유형 다시 보기, 핵심 진단 시작 |
| 이동 | 핵심 역량 진단 시작하기 → SCR-001 |
| Desktop | 4×4 그리드, 결과는 좌우 분할 |
| Mobile | 2열 그리드, 결과는 스택 |
| 금지 기능 | 핵심 100점과의 합산·가중치, 핵심 점수 스타일(`accent` 큰 숫자) 재사용, MBTI 기반 합격·채용 가능성 단정, 저장·계정 연동. 고지 필수: Intro와 결과 Section 양쪽에 "핵심 100점에 반영되지 않음" |

---

## 이동 관계 요약

```
SCR-001 ──제출──▶ SCR-002 ──추천──▶ SCR-003
   ▲                │  └──직무──▶ SCR-004 ──▶ (외부 사이트, 새 탭)
   │                └─ 근거 보기 = Drawer (같은 화면)
   └──── SCR-003/004/005 에서 다시 진단·시작 CTA
SCR-005 ──핵심 진단 시작──▶ SCR-001
SCR-002·003·004 ──진단 미완료──▶ SCR-001
Header 탭 5개: 모든 화면 → SCR-001~005
```

## 🔍 완료 조건 검증

- [x] Route 중복 없음 (5개 모두 고유)
- [x] Page Entry 중복 없음
- [x] Screen 수 5 (기술 Route는 Screen 수에 미포함)
- [x] 핵심 4개(SCR-001~004)·보조 1개(SCR-005) 구분 존재
- [x] 모든 Screen `page_owner_task_required=true`, `preview_required=true`, SCR-001 `starter_template_forbidden=true`
