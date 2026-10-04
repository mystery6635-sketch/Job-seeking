# WAVE_PLAN

`scripts/build_waves.py`가 만든 Wave 계획이다(생성 2026-10-04T03:54:34Z, 스키마 jobfit-wave-v1). Wave ID는 이 파일과 `WAVE_STATE.json`이 정본이다.

## 규칙

- Wave당 최대 7개 Task. 한 그룹이 더 크거나 같은 파일을 `modify`하는 Task가 있으면 같은 그룹을 여러 Wave로 나눈다.
- 한 Wave 안에서는 선행 Task가 먼저 오는 순서(같은 순위는 Task ID 순)로 하나씩 실행한다. Page Owner는 그 Wave의 마지막이다.
- 선행 Task는 항상 앞선 Wave 또는 같은 Wave의 앞 순서에 있다.
- `checkpoint_required`가 true인 Wave는 끝나면 사람이 Desktop·Mobile Preview를 확인한다.
- 자동 Branch·PR·Merge와 자동 수정 재시도는 없다.

## Wave 요약

| Wave | 제목 | Task 수 | Checkpoint |
|---|---|---|---|
| W01 | Scaffold·테스트 도구·Harness 확인 | 1 | - |
| W02 | 공통 UI(Token·Layout·Feedback·Section)·정적 데이터 (1/2) | 5 | - |
| W03 | 공통 UI(Token·Layout·Feedback·Section)·정적 데이터 (2/2) | 5 | - |
| W04 | 진단 로직·Supabase 4개 Table·기본 RLS (1/2) | 4 | - |
| W05 | 진단 로직·Supabase 4개 Table·기본 RLS (2/2) | 4 | - |
| W06 | SCR-001 진단 입력(API·Component·Page Owner) | 5 | 필요 |
| W07 | SCR-002 역량리포트(API·Component·Page Owner) | 6 | 필요 |
| W08 | SCR-003 직업훈련 추천(API·Component·Page Owner) | 3 | 필요 |
| W09 | SCR-004 직무추천(API·Component·Page Owner) | 3 | 필요 |
| W10 | SCR-005 직무수행태도 진단(API·Component·Page Owner) | 4 | 필요 |
| W11 | Unit·Playwright Chromium·CI (1/2) | 5 | - |
| W12 | Unit·Playwright Chromium·CI (2/2) | 5 | - |
| W13 | Vercel Preview·수동 확인·Release 확인 | 6 | 필요 |

## W01 Scaffold·테스트 도구·Harness 확인

1. `FND-TEST-TOOLING` 테스트 도구 설정(Vitest, Playwright Chromium)

Checkpoint: 없음

## W02 공통 UI(Token·Layout·Feedback·Section)·정적 데이터 (1/2)

1. `DATA-JOBSITES` 외부 구인 사이트 검색 URL 템플릿 정적 데이터
2. `DATA-MBTI-ATTITUDE` MBTI 16유형 직무 수행 태도 정적 데이터
3. `DATA-RECOMMENDATIONS` 자격증·훈련 추천 정적 데이터
4. `FND-TOKENS` D-001 Token CSS와 루트 레이아웃
5. `FND-FEEDBACK` 공통 Alert·Toast·EmptyState·Skeleton

Checkpoint: 없음

## W03 공통 UI(Token·Layout·Feedback·Section)·정적 데이터 (2/2)

1. `FND-ROOT-REDIRECT` 루트 Starter 제거와 /diagnosis redirect
2. `FND-SECTIONS` 공통 Section 컴포넌트(Intro·Hero·StepGuide·CtaBanner)
3. `FND-SESSION-GUARD` 진단 세션 저장소와 미완료 접근 Guard
4. `FND-SHELL` 공통 Header·Footer·Breadcrumb
5. `FND-NOT-FOUND` not-found 화면

Checkpoint: 없음

## W04 진단 로직·Supabase 4개 Table·기본 RLS (1/2)

1. `LIB-INPUT-VALIDATION` 진단 입력 검증
2. `DB-SCHEMA-BASE` DB 스키마(4개 테이블)
3. `DB-RLS-BASE` DB 접근 제어(RLS·서버 전용 키)
4. `LIB-JOBLINK-BUILDER` 희망 직무 → 검색 링크 생성

Checkpoint: 없음

## W05 진단 로직·Supabase 4개 Table·기본 RLS (2/2)

1. `LIB-SCORING-ENGINE` 100점 진단 점수 산출 엔진
2. `LIB-DEDUCTION-REASONS` 감점 근거 도출
3. `LIB-RECO-MAPPER` 감점 항목 기반 추천 매핑
4. `DB-ACCESS` DB 접근 함수(서버 전용)

Checkpoint: 없음

## W06 SCR-001 진단 입력(API·Component·Page Owner)

1. `API-DIAG-SUBMIT` POST /api/diagnosis (API-01)
2. `CMP-FIELDS` 입력 필드 컴포넌트(TextField·SelectField·ChipInput·NoneCheckbox)
3. `FEAT-OBS-EVENTS` KPI 이벤트 기록(진단 완료·근거 화면 도달)
4. `CMP-DIAG-FORM` 진단 입력 Form 컴포넌트
5. `PAGE-SCR001` 진단 입력 페이지 조립(Page Owner) — Page Owner(SCR-001)

Checkpoint: 필요(사람이 Preview 확인)

## W07 SCR-002 역량리포트(API·Component·Page Owner)

1. `API-DIAG-REASONS` GET /api/diagnosis/[result_id]/reasons (API-03)
2. `API-DIAG-RESULT` GET /api/diagnosis/[result_id] (API-02)
3. `CMP-DEDUCTION-CHIPS` 카테고리 Chip 목록
4. `CMP-REASON-DRAWER` 감점 근거 Drawer
5. `CMP-SCORE-HERO` 결과 Hero·게이지·입력값 요약
6. `PAGE-SCR002` 역량리포트 페이지 조립(Page Owner) — Page Owner(SCR-002)

Checkpoint: 필요(사람이 Preview 확인)

## W08 SCR-003 직업훈련 추천(API·Component·Page Owner)

1. `API-DIAG-RECOMMENDATIONS` GET /api/diagnosis/[result_id]/recommendations (API-04)
2. `CMP-RECO-GRID` 추천 Card Grid
3. `PAGE-SCR003` 직업훈련 추천 페이지 조립(Page Owner) — Page Owner(SCR-003)

Checkpoint: 필요(사람이 Preview 확인)

## W09 SCR-004 직무추천(API·Component·Page Owner)

1. `API-DIAG-JOBS` GET /api/diagnosis/[result_id]/jobs (API-06)
2. `CMP-JOB-SITES` 구인 사이트 연결 Card Grid
3. `PAGE-SCR004` 직무추천(외부 구인 사이트 검색 연결) 페이지 조립(Page Owner) — Page Owner(SCR-004)

Checkpoint: 필요(사람이 Preview 확인)

## W10 SCR-005 직무수행태도 진단(API·Component·Page Owner)

1. `API-ATTITUDE` GET /api/attitude?mbti= (API-07)
2. `CMP-ATTITUDE-PANEL` 태도 점수·강점·유의점 패널
3. `CMP-MBTI-GRID` MBTI 16유형 선택 그리드
4. `PAGE-SCR005` 직무수행태도 진단(MBTI 보조 지표) 페이지 조립(Page Owner) — Page Owner(SCR-005)

Checkpoint: 필요(사람이 Preview 확인)

## W11 Unit·Playwright Chromium·CI (1/2)

1. `E2E-DIAG-FLOW` Chromium 진단 핵심 흐름
2. `E2E-JOBS-ATTITUDE` Chromium 직무추천·태도 진단·Empty State
3. `E2E-PUBLIC-SMOKE` Chromium 공개 화면 Smoke
4. `TEST-RLS-BASIC` DB 접근 제어 기본 테스트
5. `UNIT-JOBLINK` 구인 링크 생성 단위 테스트

Checkpoint: 없음

## W12 Unit·Playwright Chromium·CI (2/2)

1. `UNIT-MBTI-MAP` MBTI 매핑 단위 테스트
2. `UNIT-REASONS-RECO` 감점 근거·추천 매핑 단위 테스트
3. `UNIT-SCORING` 점수 산출 단위 테스트
4. `UNIT-VALIDATION` 입력 검증 단위 테스트
5. `OPS-CI` CI(lint·typecheck·unit·build)

Checkpoint: 없음

## W13 Vercel Preview·수동 확인·Release 확인

1. `MANUAL-JOBLINKS` 구인 사이트 검색 URL 실사이트 확인
2. `MANUAL-PERF` 응답 시간 수동 측정
3. `OPS-VERCEL-DB-CHECK` Vercel 수동 배포와 DB 연결·플랫폼 로그 설정
4. `MANUAL-LOGS-OBS` 저장 암호화·접근 로그·KPI 이벤트 확인
5. `MANUAL-PREVIEW` Desktop·Mobile Preview 확인
6. `RELEASE-CHECK` MVP Release Criteria 점검

Checkpoint: 필요(사람이 Preview 확인)
