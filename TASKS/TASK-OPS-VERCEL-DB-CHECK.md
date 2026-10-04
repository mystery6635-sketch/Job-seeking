# TASK-OPS-VERCEL-DB-CHECK Vercel 수동 배포와 DB 연결·플랫폼 로그 설정

- Task ID: OPS-VERCEL-DB-CHECK
- Seq: 56
- Category: OPS
- Priority: P1
- Status: NOT_STARTED

## Context

Vercel 수동 배포와 DB 연결·플랫폼 로그 설정. CI 또는 배포·DB 연결 점검을 수행한다.

선행 Task: `PAGE-SCR001`, `PAGE-SCR002`, `PAGE-SCR003`, `PAGE-SCR004`, `PAGE-SCR005`, `DB-RLS-BASE`, `API-DIAG-SUBMIT`.

이 Task에 의존하는 Task: `MANUAL-PREVIEW`, `MANUAL-LOGS-OBS`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- REQ-NFR-SEC-003: 커스텀 감사 로그 대신 호스팅/DB 플랫폼 기본 접근 로그 활용(Dummy)

## Requirement Ref

- REQ-NFR-SEC-003 (IMPLEMENT) — SRS §4.4.3 (`docs/06_SRS_UIUX_REVISED.md`)

## Screen / Route / Page Entry

- Screen: —
- Route: —
- Page Entry: —

## Design Ref

- `docs/06_SRS_UIUX_REVISED.md` §4.4.3 — 시각 규칙 없음

## Depends On

- `PAGE-SCR001` — 진단 입력 페이지 조립(Page Owner)
- `PAGE-SCR002` — 역량리포트 페이지 조립(Page Owner)
- `PAGE-SCR003` — 직업훈련 추천 페이지 조립(Page Owner)
- `PAGE-SCR004` — 직무추천(외부 구인 사이트 검색 연결) 페이지 조립(Page Owner)
- `PAGE-SCR005` — 직무수행태도 진단(MBTI 보조 지표) 페이지 조립(Page Owner)
- `DB-RLS-BASE` — DB 접근 제어(RLS·서버 전용 키)
- `API-DIAG-SUBMIT` — POST /api/diagnosis (API-01)

## Expected Files

- create: TASKS/evidence/deploy-check.md
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. Vercel에 수동 배포하고 Production 환경변수(서버 전용 DB 키)를 설정한 뒤 배포 URL에서 진단 제출→결과 조회가 동작함을 확인한다
2. 관리형 DB 프로젝트에 4개 테이블·RLS가 적용되어 있음을 확인한다
3. 개인정보 접근·조회 이력은 커스텀 감사 로그 없이 Vercel 런타임 로그와 DB 플랫폼 접근 로그를 활성화해 대체한다(REQ-NFR-SEC-003, Dummy)

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. `NEXT_PUBLIC_` 변수에 서버 전용 키가 없음을 Vercel 환경변수 목록에서 확인한다

## Test Cases

- REQ-NFR-SEC-003: TC-NFR-SEC-003

## Verify

- 배포 URL 수동 확인

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목을 모두 충족했다
- [ ] Verify의 명령·확인을 실행해 결과를 기록했다(통과하지 못하면 완료로 보고하지 않는다)
- [ ] Expected Files에 없는 파일을 수정하지 않았다
- [ ] Forbidden 항목에 해당하는 변경이 없다
- [ ] 실행 결과를 기록했다

## Forbidden

- Expected Files 밖 파일 수정·생성 금지(필요하면 먼저 `TASKS/00_TASK_LIST.md`를 고친다)
- 로그인·계정·관리자·결제·별점·광고 UI·Route 추가 금지
- D-001 Token에 없는 색·간격·그림자 추가 금지
- `Lorem ipsum`·`준비 중`·`정보 확인 필요`·`TBD` 등 Placeholder 문구 금지
- 자동 Merge·EC2·AWS 설정 추가 금지
- 구현 코드·Branch·Commit을 이 문서 작업으로 만들지 않는다
- 자동 Merge·자동 배포·EC2·AWS 단계 금지
