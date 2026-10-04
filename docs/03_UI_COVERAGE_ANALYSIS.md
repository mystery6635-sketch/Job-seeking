# UI Coverage Analysis — AI 기반 구직역량 진단·매칭 서비스 (v1 MVP)

**기반 문서**: `docs/02_SRS_BASELINE.md`(전체 SRS 유지), `docs/PROJECT_SCOPE.md`

본 문서는 SRS의 모든 Requirement를 유지한 채, 3개의 고정 디자인 Screen에 UI 요구사항을 배치한다.

---

## 1. 고정 디자인 Screen (총 5개, 2026-10-03 SCR-004·SCR-005 추가)

| Screen ID | Route | 명칭 |
|---|---|---|
| SCR-001 | `/diagnosis` | 진단 입력 |
| SCR-002 | `/diagnosis/result` | 진단 결과 (감점 근거 Drawer/Modal 포함) |
| SCR-003 | `/diagnosis/result/recommendations` | 추천 리스트 |
| SCR-004 | `/diagnosis/result/jobs` | 희망 직무 기반 외부 구인정보 검색 연결 |
| SCR-005 | `/diagnosis/attitude` | MBTI 기반 직무 수행 태도 보조 지표 |

- 감점 근거 상세(원 SRS 라우트 `/diagnosis/result/reasons`)는 별도 Screen으로 세지 않고 **SCR-002의 Drawer/Modal**로 배치한다.
- API Route(`/api/diagnosis`, `/api/diagnosis/{result_id}`, `/api/diagnosis/{result_id}/reasons`, `/api/diagnosis/{result_id}/recommendations`)는 기술 Route이며 디자인 Screen으로 세지 않는다.
- 로그인/인증, 관리자 화면은 SRS §1.2.2(OS-06, OS-07)에 따라 v1 범위 밖이므로 배치할 Screen이 없다.

---

## 2. Screen 상세

### SCR-001 `/diagnosis` 진단 입력

- **사용자 목표**: 학력·나이·경력(필수)과 자격증·skill(선택)을 입력해 진단을 제출한다.
- **주요 영역**: 필수/선택 입력 필드, 오류 메시지 영역, "진단하기" 버튼
- **상태**: 초기 입력 상태 / 검증 오류 상태(필수 누락) / 제출 중 상태(버튼 비활성화) / 제출 완료
- **이동 목적지**: 제출 성공 시 SCR-002로 이동

### SCR-002 `/diagnosis/result` 진단 결과 (감점 근거 Drawer/Modal 포함)

- **사용자 목표**: 100점 만점 점수를 확인하고, 필요 시 항목별 감점 근거를 열람한다.
- **주요 영역**: 총점 표시 영역, "근거 보기" 진입점, 감점 근거 Drawer/Modal(항목별 감점 사유·"감점 없음" 표시), 추천 리스트 이동 링크
- **상태**: 결과 로딩 / 결과 표시 / 진단 미완료 접근 시 안내 상태(리다이렉트 또는 안내 메시지) / Drawer 열림·닫힘
- **이동 목적지**: "근거 보기"는 SCR-002 내 Drawer 열기(라우트 이동 아님), 추천 리스트 링크는 SCR-003으로 이동

### SCR-003 `/diagnosis/result/recommendations` 추천 리스트

- **사용자 목표**: 감점 항목 기반 자격증·훈련 추천을 확인한다.
- **주요 영역**: 추천 리스트(정적 매핑), 감점 항목 없을 때의 대체 안내 영역
- **상태**: 추천 목록 표시 / 대체 안내 표시(만점) / 진단 미완료 접근 시 안내 상태
- **이동 목적지**: SCR-002로 돌아가는 링크 제공

### SCR-004 `/diagnosis/result/jobs` 희망 직무 기반 외부 구인정보 검색 연결

- **사용자 목표**: 입력했던 희망 직무로 잡코리아·사람인·원티드·워크넷·IT 전문 구인 사이트 등에서 바로 검색해본다.
- **주요 영역**: 사이트별 연결 Card(로고/이름 + "희망 직무로 검색하기" 링크), 희망 직무 정보 없음 안내 영역
- **상태**: 연결 Card 목록 표시 / 희망 직무 미입력 안내 상태 / 진단 미완료 접근 시 안내 상태
- **이동 목적지**: 각 Card는 외부 사이트 검색 결과 페이지로 새 탭 이동(라우트 이동 아님), SCR-002/SCR-001로 돌아가는 링크 제공

### SCR-005 `/diagnosis/attitude` MBTI 기반 직무 수행 태도 보조 지표

> 핵심 역량 진단(SCR-001~004)과 독립적으로 접근 가능하며, 진단 완료 여부와 무관하게 열람할 수 있다. 표시되는 점수는 핵심 100점 점수와 절대 합산되지 않는 참고용 보조 지표다.

- **사용자 목표**: 자신의 MBTI를 선택해 직무 수행 태도 측면의 강점·유의점을 참고용으로 확인한다.
- **주요 영역**: MBTI 16유형 선택 UI, 선택 유형의 태도 점수·강점·유의점 표시 영역, "참고용 보조 지표" 고지 배너
- **상태**: MBTI 미선택 안내 상태(선택 UI만 노출) / 선택 완료 후 결과 표시 상태
- **이동 목적지**: SCR-001(핵심 역량 진단 시작)로 이동하는 CTA 제공

---

## 3. Requirement 배치 및 분류

**분류 기준**
- UI_DIRECT: 화면에 직접 표시·조작되는 요구사항
- UI_STATE: 화면의 상태(버튼 비활성화, 접근 차단 등)로 구현되는 요구사항
- NON_UI: 화면에 직접 드러나지 않는 로직·데이터 요구사항
- OPERATIONS: 운영자 작업·인프라·모니터링 성격의 요구사항

| Requirement ID | UI 분류 | PROJECT_SCOPE 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|
| REQ-FUNC-DIAG-001 | UI_DIRECT | IMPLEMENT | SCR-001(입력) → SCR-002(점수 표시) | 입력~결과 표시 전 구간 |
| REQ-FUNC-DIAG-002 | UI_DIRECT | IMPLEMENT | SCR-001 | 필수 항목 누락 오류 메시지 |
| REQ-FUNC-DIAG-003 | NON_UI | IMPLEMENT | 해당 없음(SCR-001 제출 로직 내부) | 채점 함수의 결정성, 화면에 직접 노출 안 됨 |
| REQ-FUNC-DIAG-004 | UI_STATE | IMPLEMENT | SCR-001 | 제출 중 버튼 비활성화 상태 |
| REQ-FUNC-SCORE-001 | UI_DIRECT | IMPLEMENT | SCR-002 Drawer/Modal | 감점 사유 최소 3개 표시 |
| REQ-FUNC-SCORE-002 | UI_DIRECT | IMPLEMENT | SCR-002 Drawer/Modal | 만점 항목 "감점 없음" 표시 |
| REQ-FUNC-SCORE-003 | UI_STATE | IMPLEMENT | SCR-002 | 진단 미완료 접근 차단·안내 상태 |
| REQ-FUNC-RECO-001 | UI_DIRECT | IMPLEMENT | SCR-003 | 정적 매핑 추천 리스트/대체 안내 |
| REQ-FUNC-JOBLINK-001 | UI_DIRECT | IMPLEMENT | SCR-004 | 사이트별 외부 검색 연결 Card |
| REQ-FUNC-JOBLINK-002 | UI_STATE | IMPLEMENT | SCR-004 | 희망 직무 미입력 안내 상태 |
| REQ-FUNC-ATTITUDE-001 | UI_DIRECT | IMPLEMENT | SCR-005 | MBTI 선택 UI 및 태도 점수·강점·유의점 표시, 분리 고지 |
| REQ-FUNC-ATTITUDE-002 | UI_STATE | IMPLEMENT | SCR-005 | MBTI 미선택 안내 상태 |
| REQ-FUNC-PERSONALIZE-001 | NON_UI | EXCLUDED | 배치 없음 | Post-MVP 이연, v1 화면 없음 |
| REQ-FUNC-PERSONALIZE-002 | NON_UI | EXCLUDED | 배치 없음 | Post-MVP 이연, v1 화면 없음 |
| REQ-FUNC-PERSONALIZE-003 | NON_UI | EXCLUDED | 배치 없음 | Post-MVP 이연, v1 화면 없음 |
| REQ-FUNC-ADMIN | OPERATIONS | EXCLUDED | 배치 없음 | 관리자 화면 자체가 범위 밖(OS-07) |
| REQ-NFR-PERF-001 | NON_UI | IMPLEMENT | 해당 없음(SCR-001 제출 처리 내부) | 5초 이내 응답, 수동 측정 |
| REQ-NFR-AVAIL-001 | OPERATIONS | EXCLUDED | 배치 없음 | 정식 가동률 측정 인프라 미구현 |
| REQ-NFR-SEC-001 | NON_UI | IMPLEMENT | 해당 없음 | DB 저장 암호화, 화면 비노출 |
| REQ-NFR-SEC-002 | NON_UI | IMPLEMENT | 해당 없음 | 접근 제어, 화면 비노출 |
| REQ-NFR-SEC-003 | OPERATIONS | IMPLEMENT | 배치 없음 | 호스팅/DB 기본 접근 로그(Dummy), 운영자 확인용 |
| REQ-NFR-PRIV-001 | NON_UI | IMPLEMENT | SCR-001 필드 설계 제약 | 수집 항목을 진단 필요 항목으로 한정 |
| REQ-NFR-PRIV-002 | OPERATIONS | EXCLUDED | 배치 없음 | 자동 삭제 미구현, 운영자 수동 처리 |
| REQ-NFR-OBS-001 | OPERATIONS | IMPLEMENT | 배치 없음(SCR-001/SCR-002 이벤트 트리거) | 진단 완료·근거 도달 이벤트 최소 기록(Dummy) |

---

## 4. 검사 결과

- SRS §4.3~4.4의 Requirement 총 24개(REQ-FUNC 16개 + REQ-NFR 8개, 2026-10-03 REQ-FUNC-JOBLINK-001~002·REQ-FUNC-ATTITUDE-001~002 추가)를 모두 추출·기록했다. 삭제된 Requirement는 없다.
- PROJECT_SCOPE에서 EXCLUDED로 분류된 항목(REQ-FUNC-PERSONALIZE-001~003, REQ-FUNC-ADMIN, REQ-NFR-AVAIL-001, REQ-NFR-PRIV-002)은 본 문서에서도 EXCLUDED로 유지했으며, 어떤 Screen에도 구현 범위로 배치하지 않았다.
- 디자인 Screen은 SCR-001~005 5개로 고정했으며 초과 생성하지 않았다.
- REQ-FUNC-ATTITUDE-001~002(SCR-005)는 PRD §4 차별화 문구와 충돌 소지가 있어 핵심 100점 점수와 분리된 참고용 지표로 한정 배치했다(`docs/02_SRS_BASELINE.md` IS-07, OQ-23 참조).
