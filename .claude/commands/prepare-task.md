---
description: Task 구현 착수 전 점검(Working Tree·의존성·Expected Files·Ref·환경변수·Secret·EXCLUDED)을 하고 READY/BLOCKED 판정을 낸다. 코드를 수정하지 않는다
argument-hint: "<TASK_ID> (예: PAGE-SCR002)"
allowed-tools: Read, Grep, Glob, Bash(git status:*), Bash(git log:*), Bash(git diff:*), Bash(ls:*)
---

`jobfit-project-pipeline` Skill의 규칙을 따라 구현 착수 전 점검만 한다. 대상: $ARGUMENTS

이 Command는 **어떤 파일도 수정·생성·삭제하지 않는다.** 코드 작성, `npm install`, DB 접속, `git add/commit/checkout/stash`, 감사·생성 스크립트 실행(`audit_tasks.py`, `gen_task_details.py`는 문서를 다시 쓰므로 실행 금지)을 하지 않고 읽기만 한다.

## 입력

- `TASK_ID`: 인자의 첫 단어. 비어 있으면 Task ID를 묻고 중단한다.
- 선택된 상세 Task 파일: `TASKS/TASK-<TASK_ID>.md`
- 이 프로젝트에는 Wave가 없다(DEC-010·011 보류). `WAVE_ID`가 함께 주어지면 무시하고, Wave 대신 Task 단위로 점검한다고 알린다.

## 점검

실제 파일을 읽어 확인한다. 기억이나 추정으로 판정하지 않는다.

1. **Working Tree**: `git status --porcelain`이 비어 있어야 한다. 변경·untracked 파일이 하나라도 있으면 목록을 보고한다(Task diff가 다른 변경과 섞이지 않게 하기 위함). `backup_*` 폴더도 untracked로 잡히면 목록에 포함한다.
2. **Task 포함 여부**: `TASKS/00_TASK_LIST.md`의 Task List 표에 `TASK_ID`가 정확히 한 번 있고 `Implementation Status`가 `IMPLEMENT`이며 상세 파일 `TASKS/TASK-<TASK_ID>.md`가 있어야 한다. 마지막 감사 결과(`TASKS/TASK_AUDIT_REPORT.md`의 결과 줄)가 `AUDIT_PASS`인지도 읽어서 확인한다(실행하지 않는다). 상세 파일의 Depends On·Expected Files가 Task List 행과 같은지 대조한다.
3. **Depends On 완료 여부**: 각 선행 Task의 완료 증거를 파일로 확인한다. 이 프로젝트에는 완료 상태 기록이 없으므로 다음을 증거로 쓴다.
   - 코드 Task: 선행 Task의 `create` 대상 파일이 모두 존재한다.
   - `modify`·`delete`만 있는 Task: 대상 파일 상태만으로 완료를 판단할 수 없으므로 미확인으로 보고하고 사용자 확인이 필요하다고 적는다.
   - `MANUAL`·`OPS` Task: `TASKS/evidence/`의 확인 기록 파일이 있다.
   - 증거가 없거나 미확인이면 완료로 치지 않는다.
4. **Expected Files**: `create` 대상이 이미 존재하지 않는지, `modify`·`delete` 대상이 존재하는지, 경로가 상대 경로(`..` 없음)인지, 다른 Task의 `create` 대상과 겹치지 않는지 확인한다. Page Owner는 Page Entry 하나만 가져야 한다. 이 목록 밖 파일은 수정하지 않는다는 점을 보고에 명시한다.
5. **SRS·Scope·Design·Screen Ref**: Task의 Requirement Ref가 `docs/PROJECT_SCOPE.md`에 `IMPLEMENT`로 있고 `docs/06_SRS_UIUX_REVISED.md`에 있는지, Design Ref의 문서·절(`design-reference/D-001/DESIGN.md` §번호, `UI_CONTRACT.md`의 Screen 절)이 실제로 있는지, Screen·Route·Page Entry가 `design-reference/SCREEN_ROUTE_CONTRACT.json`과 같은지 확인한다. Ref가 없거나 다르면 입력 부족이다.
6. **필요한 환경변수 이름**: Task 문서(AC·Verify·Security/Privacy AC)와 Category로 필요한 환경변수를 **이름만** 정리한다. DB·API·`TEST-RLS-BASIC`·`OPS-VERCEL-DB-CHECK`는 서버 전용 Supabase 접속 정보(제안 이름 `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, 확정은 `.env.example`)가 필요하고, UI·로직 Task(`FND-*`, `LIB-*`, `DATA-*`, `CMP-*`, `PAGE-*`)는 필요 없다. `.env.local`에 해당 이름이 있는지 `Grep`으로 이름 줄의 존재만 확인한다. **값은 읽어서 출력하지 않는다.** `.gitignore`가 `.env*`를 제외하는지도 확인한다.
7. **Secret 하드코딩 위험**: Task가 키·토큰을 코드에 넣도록 요구하는 문구가 있는지, Expected Files 중 이미 존재하는 파일과 `src/`·`db/`에 Secret 형태(`service_role`, `eyJ`로 시작하는 JWT, `sk-`, `NEXT_PUBLIC_`이 붙은 service key, 비밀번호 리터럴)가 있는지 검색한다. 발견하면 값 대신 파일·줄 번호만 보고한다.
8. **EXCLUDED 범위 침범**: Requirement Ref에 EXCLUDED 항목(`REQ-FUNC-PERSONALIZE-001~003`, `REQ-FUNC-ADMIN`, `REQ-NFR-AVAIL-001`, `REQ-NFR-PRIV-002`)이 없어야 하고, Task 문구·Expected Files에 개인화 추천(API-05), 관리자 화면, 자동 삭제 배치, 가동률 측정, 로그인·Auth, 결제·별점·광고, `/diagnosis/result/reasons` Route, 브라우저 Supabase 클라이언트, Prisma·ORM, AWS·EC2, 자동 Merge가 들어 있지 않아야 한다. "만들지 않는다" 같은 부정 문맥은 침범이 아니다.

## 출력

첫 줄에 아래 중 정확히 하나만 쓴다. 여러 항목에 걸리면 우선순위가 높은 것을 쓰고, 나머지는 아래 표에 모두 적는다.

| 판정 | 조건 | 우선순위 |
|---|---|---|
| `BLOCKED_DIRTY_TREE` | 점검 1 실패 | 1 |
| `BLOCKED_INPUT` | 점검 2·4·5·6 실패(Task·상세 파일·Ref·Expected Files·환경변수 이름·감사 결과 부족) | 2 |
| `BLOCKED_SCOPE` | 점검 7·8 실패(Secret 하드코딩 위험, EXCLUDED 침범) | 3 |
| `BLOCKED_DEPENDENCY` | 점검 3 실패(선행 Task 미완료·미확인) | 4 |
| `READY_TO_IMPLEMENT` | 8개 점검 모두 통과 | — |

이어서 다음을 보고한다.

- 점검 8개의 결과표(번호·항목·PASS/FAIL·근거 파일과 값 대신 요약)
- 막힌 이유와 풀 방법(예: 커밋 또는 변경 정리 요청, 선행 Task ID, 필요한 환경변수 이름과 등록 위치)
- `READY_TO_IMPLEMENT`이면 구현 범위 요약: Expected Files 목록, Functional·Visual·Security/Privacy AC, 검증 명령(Verify), "Expected Files 밖 파일 수정 금지"

판정은 구현을 시작하라는 승인이 아니다. 구현은 사용자가 요청할 때 `TASKS/TASK-<TASK_ID>.md`를 기준으로 시작한다.
