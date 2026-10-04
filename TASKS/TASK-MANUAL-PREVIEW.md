# TASK-MANUAL-PREVIEW Desktop·Mobile Preview 확인

- Task ID: MANUAL-PREVIEW
- Seq: 51
- Category: MANUAL
- Priority: P0
- Status: NOT_STARTED

## Context

Desktop·Mobile Preview 확인. 자동화하지 않는 항목을 수동으로 확인하고 증거를 남긴다.

선행 Task: `PAGE-SCR001`, `PAGE-SCR002`, `PAGE-SCR003`, `PAGE-SCR004`, `PAGE-SCR005`, `OPS-VERCEL-DB-CHECK`.

이 Task에 의존하는 Task: `RELEASE-CHECK`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-FUNC-SCORE-003: 진단 미완료 상태에서 근거 화면 접근 시 "먼저 진단을 완료해주세요" 안내로 전환하고 접근 차단

## Requirement Ref

- REQ-FUNC-SCORE-003 (IMPLEMENT) — SRS §4.3.2 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: —
- Route: —
- Page Entry: —

## Design Ref

- `design-reference/D-001/DESIGN.md` §15~§20, §22 검증 체크
- `design-reference/UI_CONTRACT.md` 5개 Screen 전체

## Depends On

- `PAGE-SCR001` — 진단 입력 페이지 조립(Page Owner)
- `PAGE-SCR002` — 역량리포트 페이지 조립(Page Owner)
- `PAGE-SCR003` — 직업훈련 추천 페이지 조립(Page Owner)
- `PAGE-SCR004` — 직무추천(외부 구인 사이트 검색 연결) 페이지 조립(Page Owner)
- `PAGE-SCR005` — 직무수행태도 진단(MBTI 보조 지표) 페이지 조립(Page Owner)
- `OPS-VERCEL-DB-CHECK` — Vercel 수동 배포와 DB 연결·플랫폼 로그 설정

## Expected Files

- create: TASKS/evidence/preview-check.md
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. 5개 Screen Desktop(1440), SCR-001·003 Mobile(390) Preview(OPS-VERCEL-DB-CHECK로 배포한 Vercel URL)에서 Section 순서·최소 콘텐츠 수·Empty State·가로 스크롤 없음·첫 화면 다음 Section 노출을 확인한다
2. D-001 Token 외 색 사용, 접근성(포커스 링·44px)을 확인한다

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. 화면 캡처에 실제 개인정보가 없는지 확인한다

## Test Cases

- REQ-FUNC-SCORE-003: TC-SCORE-003-F
- 이 Task가 수행하는 케이스: Functional AC 각 항목

## Verify

- 수동 확인(AC-UI-01~19)

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목을 모두 충족했다
- [ ] Verify의 명령·확인을 실행해 결과를 기록했다(통과하지 못하면 완료로 보고하지 않는다)
- [ ] Expected Files에 없는 파일을 수정하지 않았다
- [ ] Forbidden 항목에 해당하는 변경이 없다
- [ ] `TASKS/evidence/`에 확인 결과를 기록했다

## Forbidden

- Expected Files 밖 파일 수정·생성 금지(필요하면 먼저 `TASKS/00_TASK_LIST.md`를 고친다)
- 로그인·계정·관리자·결제·별점·광고 UI·Route 추가 금지
- D-001 Token에 없는 색·간격·그림자 추가 금지
- `Lorem ipsum`·`준비 중`·`정보 확인 필요`·`TBD` 등 Placeholder 문구 금지
- 자동 Merge·EC2·AWS 설정 추가 금지
- 구현 코드·Branch·Commit을 이 문서 작업으로 만들지 않는다
