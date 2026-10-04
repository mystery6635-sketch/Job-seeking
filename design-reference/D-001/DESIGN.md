# D-001 — JobFit Design System (LOCKED)

**서비스**: JobFit — AI 기반 구직역량 진단·감점 근거·훈련 추천 서비스 (v1 MVP, 로그인·결제·관리자 없음)
**대상 화면**: SCR-001 진단 입력 / SCR-002 역량리포트 / SCR-003 직업훈련 추천 / SCR-004 직무추천(외부 검색 연결) / SCR-005 직무수행태도 진단
**입력 근거**: `vendor/jobfit/DESIGN.md`(승인된 Stitch 디자인 시스템), `vendor/apple/DESIGN-apple.md`(구조 참고본), `docs/04_UIUX_PLAN.md`, `docs/STITCH_VALIDATION_REPORT.md`

> **정본 규칙**: 본 문서가 구현·화면 검수의 유일한 디자인 기준이다. 아래 Token에 없는 색·크기·반경·그림자는 사용하지 않는다.
> **참고본 차용 범위**: 참고본에서는 단일 액센트, 절제된 타이포, 여백 리듬, 얇은 헤어라인 같은 **구조 원칙만** 차용한다. 참고본의 상표·로고·서체 파일·문구는 사용하지 않는다.

---

## 1. Visual Theme

- 흰 캔버스 + 짙은 회색 텍스트 + **단일 액센트(Trust Blue)**. 한 화면에 파란 강조는 1~2곳(주 CTA, 선택 상태)으로 제한한다.
- 폼·데이터 중심 서비스이므로 사진 위주가 아니라 숫자(점수), 게이지, Chip, 아이콘으로 시각적 리듬을 만든다.
- 톤: 전문적이고 차분하며 신뢰감 있는 진단 서비스. 장식적 그라디언트·다크 모드·무거운 그림자 없음.
- 점수(100점 만점)만 크고 굵은 숫자로 표현하며, 나머지 제목은 절제된 굵기(600~700)를 쓴다.
- 문구는 모두 자연스러운 한국어 완성 문장으로 쓴다.

## 2. Color Token

| Token | 값 | 용도 |
|---|---|---|
| `color.canvas` | `#FFFFFF` | 기본 배경 |
| `color.surface-muted` | `#F7F7F5` | 교차 Section 배경, Input 비활성 배경 |
| `color.text-primary` | `#1D1D1F` | 제목·본문 |
| `color.text-secondary` | `#4A4C50` | 설명문 |
| `color.text-muted` | `#7A7A7A` | 보조 문구, placeholder |
| `color.border` | `#E3E1DD` | 헤어라인, Card·Input 테두리 |
| `color.accent` | `#1668E3` | 주 CTA, 선택 Chip, 활성 탭, 포커스 링, 링크 |
| `color.accent-hover` | `#1255BD` | accent 버튼 hover/pressed |
| `color.accent-tint` | `#E8F0FD` | 선택 Chip 배경, 활성 탭 배경 |
| `color.on-accent` | `#FFFFFF` | accent 위 텍스트 |
| `color.error` | `#D92D20` | 필수 항목 누락, 제출 실패 |
| `color.error-tint` | `#FDECEA` | 오류 Alert 배경 |
| `color.warning` | `#B54708` | 진단 미완료 접근 경고 |
| `color.warning-tint` | `#FEF3E2` | 경고 Alert 배경 |
| `color.info` | `#0E7490` | 안내·Empty State·"참고용 보조 지표" 고지 |
| `color.info-tint` | `#E4F4F8` | 안내 배너 배경 |

규칙
- accent(파랑)는 오류·경고·안내에 재사용하지 않는다. 안내/Empty/참고용 고지는 `info`(틸)만 사용한다.
- SCR-005의 "참고용 보조 지표" 영역은 `info` 계열로만 표시하고 핵심 점수 영역(`accent`)과 시각적으로 분리한다.
- "감점 있음" Chip: `accent` 채움. "감점 없음" Chip: `border` 외곽선 + `text-secondary`. 색만으로 구분하지 않고 항상 텍스트 라벨을 함께 둔다.
- 텍스트 대비 WCAG AA 이상. 위 표에 없는 색(임의 hex, 그라디언트 포함) 추가 금지.

## 3. Typography

- **Font stack**: `Inter`(Google Fonts, 오픈 라이선스 웹폰트 링크) → `Apple SD Gothic Neo` → `Malgun Gothic` → `sans-serif`. 폰트 파일을 저장소에 번들하지 않는다.
- 숫자·영문은 Inter, 한글은 시스템 한글 폰트로 렌더링된다.

| Token | Desktop | Mobile | Weight | Line-height | 용도 |
|---|---|---|---|---|---|
| `type.score` | 96px | 72px | 700 | 1.0 | 100점 만점 총점 숫자 |
| `type.h1` | 40px | 28px | 700 | 1.25 | Hero 헤드라인 |
| `type.h2` | 28px | 22px | 600 | 1.3 | Section 제목 |
| `type.h3` | 20px | 18px | 600 | 1.4 | Card·Drawer 제목 |
| `type.body-lg` | 18px | 16px | 400 | 1.6 | Hero·Section 설명 |
| `type.body` | 16px | 16px | 400 | 1.6 | 본문 |
| `type.caption` | 14px | 14px | 500 | 1.5 | Chip, 라벨, 오류 메시지 |
| `type.fine` | 12px | 12px | 400 | 1.5 | 개인정보 안내, 저작권 |

- 한글은 `word-break: keep-all`로 단어 중간 줄바꿈을 막는다. 본문 최대 줄 길이 약 40자(`max-width: 640px`).
- 본문은 400, 제목은 600~700만 사용한다. 800 이상·이탤릭·밑줄 장식 금지(링크 제외).

## 4. Spacing

8px 기반 스케일.

| Token | 값 | | Token | 값 |
|---|---|---|---|---|
| `space.1` | 4px | | `space.6` | 32px |
| `space.2` | 8px | | `space.7` | 40px |
| `space.3` | 12px | | `space.8` | 48px |
| `space.4` | 16px | | `space.9` | 64px |
| `space.5` | 24px | | `space.10` | 96px |

- Card 내부 패딩 24px(Mobile 16~20px). Card 간격 16~20px. 폼 필드 간격 16px, 필드 그룹 간격 24px.
- Section 상하 여백은 §16에서 별도로 고정한다.

## 5. Radius

| Token | 값 | 용도 |
|---|---|---|
| `radius.sm` | 8px | Button, Input, Toast |
| `radius.md` | 14px | Card, Alert, Drawer 모서리 |
| `radius.lg` | 20px | Modal, CTA Banner |
| `radius.pill` | 9999px | Chip, "진단하기" 주 CTA, 탭 |

## 6. Shadow

- 기본은 **Flat**(그림자 없음). Card는 `1px solid color.border`로 구분한다.
- 그림자는 단 한 단계만 허용: `shadow.overlay = 0 8px 24px rgba(29,29,31,0.12)` — 감점 근거 Drawer/Modal, Toast에만 사용한다.
- Drawer/Modal 뒤 Scrim: `rgba(29,29,31,0.40)`.

## 7. Header · Footer

**Header** (SCR-001~005 공통 컴포넌트, sticky, 높이 64px Desktop / 56px Mobile, 하단 1px `border`)
- 좌: JobFit 워드마크(텍스트, 이미지 로고 없음). 중앙/우: 탭 내비게이션 5개 — 진단 입력 / 역량리포트 / 직업훈련 추천 / 직무추천 / 직무수행태도 진단. 활성 탭은 `accent` 텍스트 + `accent-tint` 배경 pill.
- 우측 끝: "진단 시작하기" accent pill 버튼(항상 노출).
- Mobile(≤ 767px): 워드마크 + "진단 시작하기" + 햄버거. 탭은 햄버거 패널에 세로 목록으로 배치(항목 높이 48px).
- **Breadcrumb**: 활성 탭 명칭과 **글자 단위로 동일**해야 한다. 형식: `홈 > {탭 명칭} > {화면 부제}`.

**Footer**
- 서비스 소개 1문장, "이용안내"·"개인정보 처리방침" 링크, 저작권 표기. 배경 `surface-muted`, 상단 1px `border`.
- Desktop 2단(소개 / 링크), Mobile 1단 세로 정렬. 상하 패딩 48px.

## 8. Search · Filter

v1에는 공고 검색엔진·필터 UI가 없다. 아래 두 가지 패턴만 허용한다.
- **희망 직무 검색어 표시 바(SCR-004)**: 진단 때 입력된 희망 직무를 읽기 전용 pill로 보여주고 "직무 수정하기" 텍스트 링크를 둔다. 높이 48px, 테두리 `border`, `radius.pill`.
- **카테고리 필터 Chip(SCR-002·003)**: 학력/경력/자격증/스킬 Chip 단일 선택. Chip 높이 36px(터치 영역 44px 확보), 선택 시 `accent` 채움 + `on-accent` 텍스트.
- 결과 개수·정렬·가격·별점 필터는 두지 않는다.

## 9. Recommendation Card (Destination Card 대응)

SCR-003 훈련·자격증 Card, SCR-004 구인 사이트 연결 Card에 공통 사용한다.
- 구성(위→아래): 카테고리 태그 Chip → 제목(`type.h3`) → 1~2문장 설명(`text-secondary`) → 관련 감점 항목 태그 → CTA.
- 스타일: `canvas` 배경, 1px `border`, `radius.md`, 패딩 24px, 그림자 없음. hover 시 테두리만 `accent`로 변경.
- SCR-003 CTA: "자세히 알아보기" accent 아웃라인 버튼. SCR-004 CTA: "희망 직무로 검색하기" accent 버튼 + 외부 이동 아이콘, 새 탭으로 열림.
- 사이트명은 **텍스트로만** 표기하고 외부 서비스 로고 이미지를 사용하지 않는다. 이미지·아이콘에는 alt 텍스트를 둔다.
- Desktop 3열, Tablet 2열, Mobile 1열(간격 16~20px).

## 10. Form · Tabs

**Form (SCR-001)**
- Input·Select 높이 48px, `radius.sm`, 1px `border`, 라벨은 필드 상단(`type.caption` 600), 예시 placeholder는 `text-muted`.
- 필수 항목은 라벨에 "필수" 텍스트 표시. 포커스: 2px `accent` 링 + 2px offset. 오류: 테두리 `error` + 필드 하단 `type.caption` `error` 메시지(예: "학력을 선택해 주세요").
- 자격증·skill 입력은 Chip 입력(Enter로 추가, 각 Chip에 삭제 버튼). "없음" 체크박스를 제공하며 체크 시 입력 필드는 비활성(`surface-muted`).
- 제출 버튼 "진단하기": accent pill, 높이 52px, 제출 중에는 비활성 + 스피너 + "진단 중입니다" 텍스트.

**Tabs**
- Header 탭(상시 내비게이션) 외에 화면 내부 Tabs는 사용하지 않는다. 활성 상태는 색 + 하단 2px `accent` 바로 이중 표시한다.

**MBTI 선택 그리드(SCR-005)**
- 4×4 Card(Mobile 2×8), 각 Card에 유형 코드(예: INFJ)와 닉네임. 기본: `border`. 선택: 2px `accent` 테두리 + `accent-tint` 배경. 단일 선택, 키보드 방향키 이동 지원.

## 11. Result Item Card (Mate Post Card 대응)

게시판·메이트 모집형 Card는 v1 범위에 없다. 대응 컴포넌트는 SCR-002의 **감점 근거 항목 Card**와 SCR-005의 **강점·유의점 Card**다.
- 구성: 카테고리명(`type.h3`) → 상태 Chip("감점 있음"/"감점 없음") → 감점 점수(예: `-6점`) → 사유 문장 1~2문장.
- "감점 없음" 항목도 Card를 생략하지 않고 "해당 항목은 감점 없이 기준을 충족했습니다" 문장을 표시한다.
- 스타일은 §9 Card와 동일하며 상태 Chip만 달라진다. 작성자·좋아요·댓글·별점 요소는 두지 않는다.

## 12. Drawer · Modal

- **감점 근거 Drawer(SCR-002)**: Desktop은 우측 슬라이드 패널(폭 480px, 높이 100%), Mobile은 하단 시트(최대 높이 90vh). 라우트 변경 없이 같은 화면 위에서 열린다.
- 구성: 제목 + 닫기(X, 44px) → 카테고리 4개(학력/경력/자격증/스킬) 각각 상태 Chip과 사유 → 하단 "추천 확인하기" accent 버튼.
- `radius.md`(상단 모서리), `shadow.overlay`, Scrim `rgba(29,29,31,0.40)`. 열릴 때 포커스를 Drawer로 이동하고 Esc·Scrim 클릭으로 닫으며, 닫힌 뒤 포커스는 트리거 버튼으로 복귀한다. 포커스 트랩 필수.
- Modal은 확인이 필요한 경우(재진단 시 입력 초기화 안내)에만 사용한다. 폭 480px, `radius.lg`. 주 버튼 1개 + 취소 텍스트 링크.

## 13. Alert · Toast

| 종류 | 색 | 아이콘 | 예시 문구 |
|---|---|---|---|
| 오류 | `error` / `error-tint` | 경고 삼각형 | "필수 항목을 모두 입력해 주세요." |
| 경고 | `warning` / `warning-tint` | 느낌표 | "먼저 진단을 완료해 주세요." + "진단 입력으로 이동" CTA |
| 안내 | `info` / `info-tint` | i 원형 | "이 점수는 참고용 보조 지표이며 핵심 역량 100점에 반영되지 않습니다." |

- Alert는 Section 상단에 인라인(`radius.md`, 좌측 4px 색 바, 패딩 16px). 색과 함께 아이콘·텍스트를 항상 병행한다.
- Toast는 하단 중앙, `radius.sm`, `shadow.overlay`, 4초 후 자동 닫힘, `aria-live="polite"`. 오류 Toast는 자동으로 닫지 않는다.

## 14. Loading · Empty · Error 상태

**Loading**: 콘텐츠 형태를 닮은 Skeleton(`surface-muted`, 1.2초 pulse). 점수·목록·연결 Card 영역별로 제공. 제출 중 버튼은 비활성+스피너. `prefers-reduced-motion` 시 애니메이션 제거.

**Empty (완성형)** — 모든 Empty State는 아이콘 1개 + 제목 + 1~2문장 설명 + 다음 행동 CTA 1개를 갖춘다.

| 화면 | 상황 | 제목 / 설명 / CTA |
|---|---|---|
| SCR-003 | 만점(감점 없음) | "보완이 필요한 항목이 없습니다" / 모든 항목이 기준을 충족했으며 현재 역량을 유지하면 된다는 안내 / "결과로 돌아가기" |
| SCR-004 | 희망 직무 없음 | "희망 직무를 입력하면 채용 사이트를 바로 연결해 드립니다" / 진단 입력 시 희망 직무를 적으면 각 사이트 검색으로 이동한다는 안내 / "진단 입력하기" |
| SCR-005 | MBTI 미선택 | "내 MBTI를 선택해 보세요" / 선택하면 직무 수행 태도 보조 지표를 볼 수 있다는 안내(선택 그리드를 함께 노출) / 그리드 자체가 CTA |

**Error**: 필수 항목 누락(인라인 `error`), 진단 미완료 접근(`warning` Alert + "진단 입력으로 이동"), 데이터 로드 실패(`error` Alert + "다시 시도" 버튼). 오류 문구는 원인 + 해결 방법을 함께 쓴다.

## 15. Desktop · Mobile 규칙

| 항목 | Desktop (기준 1440px) | Mobile (기준 390px) |
|---|---|---|
| Breakpoint | ≥ 1024px | ≤ 767px (768~1023px는 Tablet: 2열) |
| 콘텐츠 최대 폭 | 1200px 중앙 정렬 (§16) | 좌우 여백 16px, 100% |
| Card Grid | 2~3열, 간격 20px | 1열, 간격 16px |
| 좌우 분할 | 5:7 또는 1:1 | 상하 스택(시각 요소가 먼저) |
| Header | 64px + 탭 노출 | 56px + 햄버거 |
| Drawer | 우측 패널 | 하단 시트 |
| 주 CTA | 인라인 pill | 폭 100%, 높이 52px |

- 터치 영역은 모든 인터랙티브 요소 44×44px 이상. 포커스 링은 항상 2px `accent`.
- 가로 스크롤 금지. 텍스트 최소 크기 14px(`type.fine` 제외).
- **Mobile 정본 화면**은 SCR-001, SCR-003이며 나머지 화면의 Mobile은 같은 규칙을 적용해 파생한다.

## 16. Page Section 최대 폭과 상하 여백

| 항목 | Desktop | Mobile |
|---|---|---|
| Section 콘텐츠 최대 폭 | **1200px** (허용 1200~1280px) | 100% − 좌우 16px |
| 본문 텍스트 블록 최대 폭 | 640px | 100% |
| Section 상하 여백 | **80px** (허용 64~96px) | **48px** (허용 40~64px) |
| Section 내부 제목→설명 | 12px | 8px |
| 설명→본문 | 32px | 24px |
| 본문→CTA | 32px | 24px |

- Section 배경은 `canvas`와 `surface-muted`를 교대로 사용해 구분선 없이 리듬을 만든다.

## 17. Hero 높이와 첫 화면 규칙

- Hero 높이: Desktop **360~480px**, Mobile **280~360px**. 뷰포트 전체 높이(100vh)를 채우지 않는다.
- 1440×900 뷰포트에서 **다음 Section의 제목 또는 상단 20% 이상이 첫 화면에 보여야 한다.** Mobile(390×844)에서도 Hero 하단 뒤로 다음 Section 상단이 보인다.
- Hero 구성: 헤드라인(`type.h1`) + 1~2문장 설명 + 주 CTA 1개(또는 점수 숫자). 보조 일러스트는 선택이며 높이를 늘리지 않는다.
- SCR-002 결과 Hero는 `type.score` 숫자 + 점수 구간 코멘트 + 게이지를 같은 높이 범위에 담는다.

## 18. Section별 위계와 시각적 리듬

모든 Section은 **제목(h2) → 설명(1~3문장) → 본문 → CTA** 순서를 따른다. 본문이 폼·결과 자체인 Section은 CTA를 제출 버튼으로 대신할 수 있다.

리듬 규칙
- 같은 형태(Card Grid)를 2개 Section 연속 배치하지 않는다. Hero → Form Card → 좌우 분할 → Chip 목록 → 3단계 안내 → CTA Banner 등 **형태를 교차**한다.
- 배경은 `canvas` ↔ `surface-muted`를 교대하고, CTA Banner만 `accent-tint` 배경 + `radius.lg`를 쓴다.
- 3단계 안내는 번호(원형 32px, `accent`) + 아이콘 + 1문장 설명 구조를 쓴다.
- 한 Section에 CTA는 최대 1개(주) + 1개(보조 텍스트 링크).

## 19. 화면별 Section 순서와 최소 콘텐츠 수

| Screen | Section 수 | 순서 | 최소 콘텐츠 |
|---|---|---|---|
| SCR-001 진단 입력 | 5 | Hero → 필수 정보 Form(학력·나이·경력) → 선택 정보 Form(자격증·skill) → 진단 3단계 안내 → 제출 CTA Banner | 필수 필드 3개, 선택 필드 2개, 안내 단계 3개 |
| SCR-002 역량리포트 | 6~7 | 결과 Hero(점수) → 좌우 분할(게이지 + 입력값 요약) → 감점 근거 진입 CTA → 카테고리 Chip 목록 → (Drawer) → 추천 이동 CTA Banner → 재진단 안내 | 카테고리 4개, 감점 사유 문장 각 1개 이상(총 4개) |
| SCR-003 직업훈련 추천 | 5 | Intro → 추천 Card Grid → 감점 없음 Empty State(미리보기 상태) → 활용 3단계 안내 → CTA Banner | **추천 Card 6개 이상**, 3단계 |
| SCR-004 직무추천 | 4 | Intro → 구인 사이트 연결 Card Grid → 희망 직무 없음 Empty State → CTA Banner | **연결 Card 6개 이상**, 고지 문장 1개 |
| SCR-005 직무수행태도 진단 | 4 | Intro(참고용 고지) → MBTI 16유형 그리드 → 태도 점수·강점·유의점 → CTA Banner | **유형 Card 16개**, 강점 2개 이상, 유의점 1개 이상 |

- Card Grid·Timeline·Gallery형 Section은 위 최소 개수에 미달하면 렌더링하지 않고 해당 화면 Empty State로 대체한다.
- SCR-003·004의 Empty State는 Card Grid와 **상호 배타 노출**이 원칙이며, 디자인 시안에서는 "미리보기" 라벨로 병기할 수 있다.
- Breadcrumb 2번째 구간은 활성 탭 명칭과 동일하게 맞춘다(SCR-004 "직무추천", SCR-005 "직무수행태도 진단").

## 20. 완성형 Empty State · Placeholder 금지 규칙

금지: `Lorem ipsum`, `준비 중`, `정보 확인 필요`, `TBD`, `추후 제공`, `샘플 텍스트`, 내용 없는 회색 박스·빈 Card, 의미 없는 이미지 자리.

필수
- 모든 Card·Chip·Drawer 항목에 실제 한국어 콘텐츠(구체적 자격증·과정·사이트·유형명)를 채운다.
- Empty State는 §14의 4요소(아이콘·제목·설명·CTA)를 갖춘다.
- 입력 필드의 placeholder는 **예시 값**(예: "예: 컴퓨터활용능력 1급")만 허용하고 "입력하세요" 단독 문구는 쓰지 않는다.
- 이미지는 목적이 있고 alt 텍스트가 있을 때만 사용한다.

## 21. Do / Do Not

**Do**
- 모든 색·간격·반경·그림자는 본 문서 Token에서만 선택한다.
- 점수는 `type.score`로 가장 크게, 감점 근거는 Chip + 사유 문장으로 근거를 함께 보여준다.
- SCR-005 고지("핵심 100점에 합산되지 않음")를 Intro와 결과 Section에 모두 노출한다.
- SCR-004에는 "특정 공고를 선별·추천하지 않으며 검색창 채움 용도로만 사용됩니다" 고지를 둔다.
- 외부 링크는 새 탭 + 외부 이동 아이콘 + `rel="noopener noreferrer"`.
- 키보드 포커스 링, 44px 터치 영역, `aria-live`, Drawer 포커스 트랩을 구현한다.

**Do Not**
- Airbnb 등 외부 서비스의 상표·로고·고유 문구·고유 UI 요소를 쓰지 않는다. 구인 사이트 로고 이미지도 쓰지 않는다.
- 구매·예약·결제·구독·체크아웃 UI(가격, 장바구니, 결제 버튼, 쿠폰)를 만들지 않는다.
- 별점·리뷰 점수·광고 배너·실시간 공고 feed·관리자 Dashboard·통계 차트를 만들지 않는다.
- Proprietary 폰트 파일을 저장소에 넣거나 `@font-face`로 서빙하지 않는다(Inter는 Google Fonts 링크만).
- Token 표에 없는 임의 색상·그라디언트·추가 그림자를 도입하지 않는다.
- accent(파랑)를 오류·경고·안내 용도로 쓰지 않으며, 참고용 보조 지표(SCR-005)를 핵심 점수 스타일로 표시하지 않는다.
- 로그인·계정·개인화·관리자 UI를 배치하지 않는다(v1 범위 밖).

---

## 22. 🔍 검증 체크

- [ ] 사용 색상이 모두 §2 Token에 있는가
- [ ] Section 상하 여백·최대 폭이 §16 범위인가 (Desktop 64~96px / Mobile 40~64px, 1200~1280px)
- [ ] 1440px에서 Hero 아래 다음 Section이 보이는가
- [ ] 화면별 Section 수·순서·최소 콘텐츠 수가 §19와 일치하는가
- [ ] Breadcrumb 명칭이 활성 탭 명칭과 같은가
- [ ] Placeholder·Lorem ipsum·빈 Card가 없는가 (§20)
- [ ] 상표·결제·별점·광고·Proprietary 폰트가 없는가 (§21)
