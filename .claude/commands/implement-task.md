---
description: prepare-task가 READY_TO_IMPLEMENT인 Task 하나를 Expected Files 안에서 구현하고 검증·보고한다. 기본적으로 Commit·Push·PR을 하지 않는다
argument-hint: "<TASK_ID> [commit]"
---

`jobfit-project-pipeline` Skill과 루트 `CLAUDE.md`의 규칙을 따라 Task 하나를 구현한다. 대상: $ARGUMENTS

첫 단어는 `TASK_ID`(예: `LIB-SCORING-ENGINE`)이고, 뒤에 `commit`이 있으면 사용자가 Task 단위 Commit을 요청한 것이다. 이 프로젝트에는 Wave가 없으므로(DEC-010·011 보류) Task 하나씩 구현한다. `TASK_ID`가 없거나 여러 개이면 하나만 지정해 달라고 하고 중단한다.

## 1. 착수 점검 (prepare-task)

구현 전에 `.claude/commands/prepare-task.md`의 점검 8개를 읽기 전용으로 수행한다(Working Tree, Task 포함 여부, Depends On 완료, Expected Files, SRS·Scope·Design·Screen Ref, 환경변수 이름, Secret 위험, EXCLUDED 침범).

- 판정이 `READY_TO_IMPLEMENT`가 아니면 **아무것도 수정하지 않고** 판정과 막힌 이유만 보고한 뒤 중단한다. 점검을 건너뛰거나 막힌 항목을 임의로 풀지 않는다(예: 더러운 작업 트리를 정리하려고 stash·reset을 쓰지 않는다).
- 여러 Task를 한꺼번에 구현하지 않는다. 선행 Task가 미완료면 그 Task를 대신 구현하지 않는다.

## 2. 읽기

- `TASKS/TASK-<TASK_ID>.md` 전체(Context, Requirement Ref, Design Ref, Depends On, Expected Files, 세 AC, Test Cases, Verify, Definition of Done, Forbidden)를 읽는다.
- 상세 파일이 가리키는 근거(`docs/06_SRS_UIUX_REVISED.md` 해당 조항, `design-reference/UI_CONTRACT.md` 해당 Screen, `design-reference/D-001/DESIGN.md` 해당 절)와 현재 파일 트리를 읽는다.
- `PAGE`·`COMPONENT`·`API`·`FOUNDATION` Task는 코드를 쓰기 전에 `package.json`과 `node_modules/next/dist/docs/`의 관련 문서를 읽는다. 이 Next.js 버전은 기존 지식과 다르다.

## 3. 구현

1. **Expected Files 안에서만 작업한다.** `create`·`modify`·`delete` 대상 외의 파일은 만들거나 고치거나 지우지 않는다. 더 필요한 파일이 생기면 구현을 멈추고 `TASKS/00_TASK_LIST.md`를 먼저 고쳐야 한다고 보고한다. 범위를 임의로 넓히지 않는다.
2. **세 AC를 따른다.** Functional AC, Visual AC(D-001 Token만 사용), Security/Privacy AC를 모두 충족한다. 충족하지 못하는 항목은 숨기지 않고 보고한다.
3. **Page Owner(`PAGE-SCR00x`)는 실제 Page Entry를 조립한다.** import뿐 아니라 상태 전환(미완료 경고, 로딩, Empty State 등)까지 연결한다. 하위 Component·API·Data 파일을 새로 만들지 않으며 Starter 템플릿이나 임시 화면을 두지 않는다. `Lorem ipsum`·`준비 중` 같은 Placeholder 문구와 큰 빈 영역은 금지다.
4. **불변조건**: 진단 입력은 `POST /api/diagnosis`로만 서버에 보내고 URL·로그·분석 이벤트·외부 사이트로 보내지 않는다. 브라우저 Supabase 클라이언트와 RLS 우회 코드를 만들지 않고, Service Role Key는 서버 전용 환경변수로만 쓴다. 키·토큰을 코드에 직접 쓰지 않고 환경변수 값을 출력하지 않는다. MBTI 지표를 100점에 합산하지 않는다.
5. **금지**: AWS·EC2, Prisma 등 ORM, 자동 Merge·merge queue, CMS·외부 Email 공급자·Monitoring, EXCLUDED 기능을 추가하지 않는다. `npm install`은 Expected Files에 `package.json`이 있고 Task AC가 요구한 패키지일 때만 한다.
6. 구현하지 않은 것을 구현했다고 기록하지 않는다. Task 문서(`TASKS/*`)의 상태나 내용을 구현 완료에 맞춰 고치지 않는다.

## 4. 검증

해당하는 것만 실제로 실행하고 결과를 그대로 기록한다. 실패를 숨기거나 기준을 완화하지 않는다.

1. 포맷·정적 검사: `npm run lint`, `npx tsc --noEmit`. 코드 Task는 `npm run build`도 실행한다.
2. **관련 Unit Test**: Task의 Verify·Test Cases가 가리키는 Vitest 테스트를 실행한다(`npm run test -- --run <패턴>`). 테스트 도구가 아직 없으면(`FND-TEST-TOOLING` 미완료) 그 사실을 보고한다.
3. **Playwright는 Page Owner 또는 E2E Task일 때만** Chromium으로 실행한다(`npx playwright test --project=chromium <spec>`). 관련 spec이 아직 없으면 실행했다고 쓰지 않고 "spec 없음"으로 보고한다. 다른 Category에서는 Playwright를 실행하지 않는다. Firefox·WebKit은 쓰지 않는다.
4. `MANUAL` Task와 Page Owner의 Desktop(1440)·Mobile(390) Preview 확인은 사람이 해야 한다. 확인한 척하지 않고 확인이 필요하다고 보고한다.
5. **Diff 확인**: `git status`와 `git diff`로 변경된 파일이 모두 Expected Files 안에 있는지 확인한다. 범위 밖 변경을 발견하면 destructive Git 명령(`reset`, `checkout --`, `clean`) 없이 직접 되돌리고 무엇을 되돌렸는지 보고한다.

`python scripts/audit_tasks.py`는 구현 전·후 모두 통과하도록 `create` 대상이 이미 있어도, `delete` 대상이 이미 없어도 오류로 보지 않는다. 다만 감사는 `TASKS/TASK_MANIFEST.csv`와 `TASKS/TASK_AUDIT_REPORT.md`를 다시 쓰므로 이 Command에서는 실행하지 않는다(Expected Files 밖 변경이 된다). 사용자가 요청하면 구현 후에 따로 실행한다.

## 5. 완료 보고

다음을 보고한다.

- **변경 파일**: 파일별 `create`/`modify`/`delete`와 한 줄 설명. Expected Files와 일치하는지.
- **검증**: 실행한 명령과 통과·실패, 실행하지 못한 검증과 이유(예: 환경변수 없음, spec 없음, 사람 확인 필요).
- **AC 충족**: Functional·Visual·Security/Privacy AC별 충족 여부.
- **제약·남은 일**: 미충족·보류 항목, 사람이 확인할 것(Preview), 다음 Task에 영향을 주는 사항.

통과하지 못한 검증이 있으면 완료라고 하지 않고 "미완료"로 보고한다.

## 6. Commit·Push·PR

- 기본은 Commit·Push·PR을 **하지 않는다.** 구현 결과는 작업 트리에 남긴다. 자동 PR·자동 Merge는 어떤 경우에도 실행하지 않는다.
- 사용자가 `commit`을 요청한 경우에만 **Task 단위 Commit 하나**까지 수행한다.
  - 검증을 통과했고 변경이 Expected Files 안에 있을 때만 한다.
  - `git add -A`를 쓰지 않고 Expected Files 경로만 지정해 stage한다.
  - 메시지는 `<TASK_ID>: <Task 제목>` 형식으로 쓰고 필요한 trailer(공동 작성 표기)를 붙인다. Hook을 우회(`--no-verify`)하지 않는다.
  - Push, PR 생성, Merge는 하지 않으며 사용자가 직접 한다.
