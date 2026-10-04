# DESIGN MANIFEST

| 항목 | 값 |
|---|---|
| **Active Design Version** | D-001 |
| **Status** | LOCKED |
| **Active File** | `design-reference/D-001/DESIGN.md` |
| **Vendor Reference** | `design-reference/vendor/airbnb/DESIGN.md` (지정값 — 현재 저장소에 파일 없음, 아래 미해결 사항 1 참고) |
| **Approved Screens** | SCR-001 ~ SCR-005 |
| **Mobile Variants** | SCR-001, SCR-003 |
| **Service** | JobFit (job-seeking, 구직역량 진단) |
| **Locked Date** | 2026-10-03 |

## 변경 규칙
- `LOCKED` 상태에서는 D-001을 수정하지 않는다. 변경이 필요하면 `D-002/DESIGN.md`를 새로 만들고 본 Manifest의 Active 항목만 갱신한다.
- 구현·Stitch 재생성·화면 검수는 Active File만 기준으로 한다. Vendor Reference는 직접 구현 기준이 아니다.

## 승인 Screen (Stitch Project `13615029693301324722`)

| Screen | Desktop ID | Mobile ID | 검증 상태 |
|---|---|---|---|
| SCR-001 진단 입력 | `75c928ba102d4f89822f48b567b15ffc` | `23f928be18f74970921b9d13a34cc0f2` | PASS |
| SCR-002 역량리포트 | `7ed01ac2331d47cf8c327a1dd93c76e8` | `94d479ecd3de4247857d1b6cbfedfb1d` | PASS |
| SCR-003 직업훈련 추천 | `ebf68715a774433baaf64a5092c74bec` | `2eb99d8bd38c4db89d7d8fc9643988f5` | PASS |
| SCR-004 직무추천 | `c48749865ebf4994806327d1798e786c` | `787abfc420f34e18a2a50fd909e0069a` | 브레드크럼 수정 필요 |
| SCR-005 직무수행태도 진단 | `0341e77537b34eb58c5a80f471d891fe` | `27325065362f402bb7da7822372a0ca2` | 브레드크럼 수정 필요 |

Mobile 정본은 SCR-001, SCR-003이며, 나머지 Mobile 화면은 D-001 §15 규칙으로 파생한다.

## 미해결 사항 (확인 필요)
1. **Vendor Reference 불일치**: `vendor/airbnb/DESIGN.md`는 저장소에 없다(`vendor/apple/DESIGN-apple.md`, `vendor/jobfit/DESIGN.md`만 존재). D-001은 apple 참고본의 구조 원칙과 승인된 `vendor/jobfit/DESIGN.md`를 근거로 작성했다. 지정 경로에 파일을 추가하거나 Manifest 값을 `vendor/apple/DESIGN-apple.md`로 바꿀지 결정이 필요하다.
2. **액센트 색 충돌**: `docs/04_UIUX_PLAN.md`는 코랄(`#ff6f59`), 승인된 `vendor/jobfit/DESIGN.md`는 Trust Blue(`#1668E3`)다. D-001은 승인된 Stitch 디자인 시스템 기준으로 **Blue**를 채택했다. 04_UIUX_PLAN.md의 코랄·info 색(`#175cd3`) 표기는 별도 정정이 필요하다.
3. **Stitch 검증 보류**: SCR-004, SCR-005 브레드크럼 문구 불일치는 Stitch 웹 UI에서 수동 수정해야 한다(`docs/STITCH_VALIDATION_REPORT.md` 참조). D-001 §19에서 올바른 명칭을 규정해 두었다.
4. **Mobile Variants 범위**: 요청 지침에 따라 SCR-001, SCR-003으로 기록했다. Stitch에는 5개 Mobile이 모두 존재한다.
