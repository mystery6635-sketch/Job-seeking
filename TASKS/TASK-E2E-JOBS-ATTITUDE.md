# TASK-E2E-JOBS-ATTITUDE Chromium 직무추천·태도 진단·Empty State

- Task ID: E2E-JOBS-ATTITUDE
- Seq: 49
- Category: E2E
- Priority: P0
- Status: NOT_STARTED

## Context

Chromium 직무추천·태도 진단·Empty State. Playwright(Chromium)로 핵심 흐름을 확인한다.

선행 Task: `PAGE-SCR003`, `PAGE-SCR004`, `PAGE-SCR005`, `FND-TEST-TOOLING`.

이 Task에 의존하는 Task: `RELEASE-CHECK`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-JOBLINK-001: 희망 직무 문자열을 사이트별 검색 URL 템플릿에 치환해 잡코리아·사람인·원티드·워크넷·IT 전문 구인 사이트 링크를 새 탭으로 연결(매칭·추천 로직 없음)
- REQ-FUNC-JOBLINK-002: 희망 직무 정보 없음 시 안내 문구와 재진단 CTA 표시
- REQ-FUNC-ATTITUDE-001: MBTI 16유형별 직무 수행 태도 점수·강점·유의점 정적 매핑 조회, 핵심 점수와 분리 고지
- REQ-FUNC-ATTITUDE-002: MBTI 미선택 시 선택 유도 안내와 선택 UI 표시
- REQ-FUNC-RECO-001: `src/data` 하드코딩 정적 매핑 테이블로 감점 항목 기반 추천 리스트 제공, 감점 항목 없으면 대체 안내

## Requirement Ref

- REQ-FUNC-JOBLINK-001 (IMPLEMENT) — SRS §4.3.3b (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-JOBLINK-002 (IMPLEMENT) — SRS §4.3.3b (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-ATTITUDE-001 (IMPLEMENT) — SRS §4.3.3c (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-ATTITUDE-002 (IMPLEMENT) — SRS §4.3.3c (`docs/06_SRS_UIUX_REVISED.md`)
- REQ-FUNC-RECO-001 (IMPLEMENT) — SRS §4.3.3 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: —
- Route: —
- Page Entry: —

## Design Ref

- `docs/06_SRS_UIUX_REVISED.md` §4.3.3c, §4.3.3c, §4.3.3b, §4.3.3b, §4.3.3 — 시각 규칙 없음

## Depends On

- `PAGE-SCR003` — 직업훈련 추천 페이지 조립(Page Owner)
- `PAGE-SCR004` — 직무추천(외부 구인 사이트 검색 연결) 페이지 조립(Page Owner)
- `PAGE-SCR005` — 직무수행태도 진단(MBTI 보조 지표) 페이지 조립(Page Owner)
- `FND-TEST-TOOLING` — 테스트 도구 설정(Vitest, Playwright Chromium)

## Expected Files

- create: tests/e2e/jobs-attitude.spec.ts
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. SCR-004: 희망 직무 입력 시 Card 6개 이상이고 링크가 `target=_blank`·`rel` 포함, 희망 직무 없음이면 Empty State와 `진단 입력하기` CTA
2. SCR-003: 만점 입력 시 Empty State와 `결과로 돌아가기` CTA
3. SCR-005: 미선택 Empty State, 유형 선택 후 강점·유의점과 `핵심 100점에 반영되지 않음` 고지 2곳

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. 외부 사이트로 실제 이동하지 않고 `href`만 검증한다

## Test Cases

- REQ-FUNC-JOBLINK-001: TC-JOBLINK-001-N
- REQ-FUNC-JOBLINK-002: TC-JOBLINK-002-F
- REQ-FUNC-ATTITUDE-001: TC-ATTITUDE-001-N
- REQ-FUNC-ATTITUDE-002: TC-ATTITUDE-002-F
- REQ-FUNC-RECO-001: TC-RECO-001-DRAFT
- 이 Task가 수행하는 케이스: Functional AC 각 항목

## Verify

- `npx playwright test --project=chromium tests/e2e/jobs-attitude.spec.ts`

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목을 모두 충족했다
- [ ] Verify의 명령·확인을 실행해 결과를 기록했다(통과하지 못하면 완료로 보고하지 않는다)
- [ ] Expected Files에 없는 파일을 수정하지 않았다
- [ ] Forbidden 항목에 해당하는 변경이 없다
- [ ] Chromium project에서만 실행해 통과한다

## Forbidden

- Expected Files 밖 파일 수정·생성 금지(필요하면 먼저 `TASKS/00_TASK_LIST.md`를 고친다)
- 로그인·계정·관리자·결제·별점·광고 UI·Route 추가 금지
- D-001 Token에 없는 색·간격·그림자 추가 금지
- `Lorem ipsum`·`준비 중`·`정보 확인 필요`·`TBD` 등 Placeholder 문구 금지
- 자동 Merge·EC2·AWS 설정 추가 금지
- 구현 코드·Branch·Commit을 이 문서 작업으로 만들지 않는다
- Firefox·WebKit project 추가 금지
- 외부 사이트로 실제 이동하는 검증 금지
