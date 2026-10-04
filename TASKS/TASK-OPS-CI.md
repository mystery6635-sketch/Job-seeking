# TASK-OPS-CI CI(lint·typecheck·unit·build)

- Task ID: OPS-CI
- Seq: 55
- Category: OPS
- Priority: P1
- Status: NOT_STARTED

## Context

CI(lint·typecheck·unit·build). CI 또는 배포·DB 연결 점검을 수행한다.

선행 Task: `FND-TEST-TOOLING`, `UNIT-SCORING`, `UNIT-VALIDATION`, `UNIT-REASONS-RECO`, `UNIT-JOBLINK`, `UNIT-MBTI-MAP`.

이 Task에 의존하는 Task: `RELEASE-CHECK`.

## Project Scope

v1 MVP 범위(`docs/PROJECT_SCOPE.md` §1~§3)를 따른다. 로그인·관리자·결제·개인화·채용공고 매칭은 제외 범위다.
- 이 Task는 특정 Requirement에 직접 대응하지 않는 지원 Task이며, 연결된 Task를 가능하게 하는 범위로 한정한다.

## Requirement Ref

- 없음 (지원 Task)

## Screen / Route / Page Entry

- Screen: —
- Route: —
- Page Entry: —

## Design Ref

- `docs/06_SRS_UIUX_REVISED.md` 관련 조항 — 시각 규칙 없음

## Depends On

- `FND-TEST-TOOLING` — 테스트 도구 설정(Vitest, Playwright Chromium)
- `UNIT-SCORING` — 점수 산출 단위 테스트
- `UNIT-VALIDATION` — 입력 검증 단위 테스트
- `UNIT-REASONS-RECO` — 감점 근거·추천 매핑 단위 테스트
- `UNIT-JOBLINK` — 구인 링크 생성 단위 테스트
- `UNIT-MBTI-MAP` — MBTI 매핑 단위 테스트

## Expected Files

- create: .github/workflows/ci.yml
- 위 목록 밖 파일은 수정하지 않는다(Expected Files 밖 수정 금지)

## Functional AC

1. PR에서 `npm run lint`, `tsc --noEmit`, `npm run test -- --run`, `npm run build`를 실행한다
2. 자동 Merge·자동 배포·EC2·AWS 단계를 만들지 않는다. Playwright E2E는 CI에 넣지 않고 수동 `npm run e2e`로 실행한다

## Visual AC

1. 해당 없음

## Security/Privacy AC

1. CI에 DB 운영 키를 넣지 않는다(테스트 DB 키는 저장소 Secret으로만)

## Test Cases

- 대응하는 SRS Test Case 없음 — 검증은 Verify의 명령·확인 항목으로 한다

## Verify

- CI 실행 결과

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
