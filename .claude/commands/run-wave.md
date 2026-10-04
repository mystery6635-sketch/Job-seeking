---
description: WAVE_PLAN의 Wave 하나를 Task 단위로 순차 실행한다(prepare → implement → 검증 → 상태 갱신). status·resume·dry-run을 지원한다. 자동 Branch·PR·Merge는 하지 않는다
argument-hint: "W03 | status | resume | dry-run W03"
---

`jobfit-project-pipeline` Skill과 루트 `CLAUDE.md`의 규칙을 따라 Wave를 실행한다. 인자: $ARGUMENTS

## 지원 명령

| 명령 | 동작 | 파일 수정 |
|---|---|---|
| `/run-wave W03` | W03의 READY Task를 순서대로 구현한다 | 앱 코드(각 Task의 Expected Files), `TASKS/WAVE_STATE.json` |
| `/run-wave status` | 모든 Wave와 Task의 상태를 표로 보여준다 | 없음 |
| `/run-wave resume` | 중단된 Wave를 이어서 실행하거나, `WAITING_FOR_PREVIEW`를 해제한다 | `/run-wave W03`과 같음 |
| `/run-wave dry-run W03` | 실행하면 처리될 Task 순서와 첫 Task의 prepare 판정만 보여준다 | 없음 |

인자가 위 형식이 아니면 사용법을 보여주고 중단한다. Wave ID는 `WAVE_PLAN`에 정의된 것만 쓴다.

## 선행 조건과 파일

이 프로젝트에는 아직 Wave가 정의되어 있지 않다(결정 DEC-010·011). 이 Command는 아래 두 파일이 **실제로 있을 때만** 동작한다. 없으면 어떤 것도 만들거나 추측하지 않고, 없는 파일을 알려준 뒤 중단한다. Wave 구성(어떤 Task를 어느 Wave에 묶을지)은 사용자가 정한다.

**`TASKS/WAVE_PLAN.md`** (정본, 사람이 작성·승인)
```
| Wave | 이름 | Task IDs (실행 후보) | Preview Checkpoint |
|---|---|---|---|
| W01 | 기반 | `FND-TEST-TOOLING`, `FND-TOKENS`, ... | 없음 |
| W03 | 진단 입력 화면 | `CMP-FIELDS`, `CMP-DIAG-FORM`, `PAGE-SCR001` | SCR-001 Desktop·Mobile Preview |
```
- Task ID는 `TASKS/00_TASK_LIST.md`의 구현 Task여야 하며 한 Task는 한 Wave에만 속한다. EXCLUDED 요구사항의 Task는 없다.
- Wave 순서는 표의 위에서 아래다. 한 Wave 안의 실행 순서는 Task의 `Depends On`이 정하고, 같은 순위면 Task List의 Seq가 앞선 것이 먼저다.
- `Preview Checkpoint`는 사람이 확인해야 하는 대상(Screen, Desktop 1440·Mobile 390)이다. 비어 있거나 `없음`이면 Checkpoint가 없다.

**`TASKS/WAVE_STATE.json`** (이 Command가 갱신하는 유일한 Task 외 파일)
```
{ "waves": { "W03": { "status": "IN_PROGRESS", "preview_confirmed": false } },
  "tasks": { "PAGE-SCR001": { "status": "DONE", "files": ["src/app/diagnosis/page.tsx"],
             "verified": ["npm run lint", "npx tsc --noEmit"], "note": "" } } }
```
- Task status: `PENDING`, `IN_PROGRESS`, `DONE`, `BLOCKED`(사유 판정 포함), `FAILED`(검증 실패)
- Wave status: `NOT_STARTED`, `IN_PROGRESS`, `WAITING_FOR_PREVIEW`, `DONE`
- `files`는 그 Task가 변경한 파일 목록이며 아래 "작업 트리 허용 범위" 계산에 쓴다.
- 파일이 없으면 모든 Task가 `PENDING`인 것으로 보고, 첫 `/run-wave` 실행 때 만든다. 파일이 깨져 있으면 추측해서 고치지 않고 중단한다.

## `/run-wave W03` 동작

0. **시작 조건**: Wave가 `WAVE_PLAN`에 있고, 앞선 Wave가 모두 `DONE`이어야 한다. 앞선 Wave가 `WAITING_FOR_PREVIEW`이면 사람의 Preview 확인(`/run-wave resume`)이 먼저라고 안내하고 중단한다. 이미 `DONE`인 Wave는 다시 실행하지 않는다.
1. **읽기**: `WAVE_PLAN`과 `WAVE_STATE`를 읽고, 현재 Wave의 Task 상태를 계산한다.
2. **Task 선택**: 현재 Wave에서 `PENDING`이고 모든 `Depends On`이 `DONE`(이전 Wave 포함)인 Task를 READY로 본다. READY Task 중 `Depends On` 순서(동순위는 Seq 순)로 **하나만** 고른다. 선행 Task가 `BLOCKED`·`FAILED`이면 그 아래 Task는 READY가 아니다.
3. **prepare-task 규칙으로 검사**: `.claude/commands/prepare-task.md`의 점검 8개를 수행한다. 아래 두 가지만 다르다.
   - Depends On 완료 증거는 파일 존재가 아니라 `WAVE_STATE`의 `DONE`이다. `WAVE_STATE`에 없는 선행 Task는 완료로 보지 않는다.
   - Working Tree는 "작업 트리 허용 범위"로 판정한다(바로 아래).
   `READY_TO_IMPLEMENT`가 아니면 Task를 `BLOCKED`(판정 이름과 사유 기록)로 갱신하고 Wave를 중단한 뒤 보고한다. 막힌 Task를 건너뛰고 다른 Task를 임의로 진행하지 않는다.
4. **implement-task 규칙으로 구현**: `.claude/commands/implement-task.md`의 읽기·구현·검증 규칙(Expected Files 안에서만 작업, 세 AC, Page Owner는 실제 Page Entry 조립, 금지 사항)으로 Task **하나**를 구현한다. 시작 전 Task를 `IN_PROGRESS`로 기록한다. `implement-task`의 Commit 규칙은 적용하지 않는다(이 Command는 Commit하지 않는다).
5. **상태 갱신**: 관련 검증(lint, 타입 검사, 해당 Unit Test, Page Owner·E2E Task의 Chromium Playwright)을 **모두 실행해 PASS**하면 `DONE`으로 바꾸고 변경 파일과 실행한 검증을 `WAVE_STATE`에 기록한다. 실패한 검증이 있으면 `FAILED`로 기록하고 Wave를 중단한다. 환경변수·도구 부족 등으로 실행하지 못한 검증이 있으면 `DONE`이 아니라 `BLOCKED`(BLOCKED_INPUT)로 기록하고 중단한다. 검증을 건너뛰고 `DONE`으로 쓰지 않는다.
6. **다음 Task**: 같은 Wave에서 다음 READY Task를 2~5로 계속 처리한다. 한 번에 하나만 구현한다.
7. **종료(전부 DONE)**: Wave의 모든 Task가 `DONE`이고 Preview Checkpoint가 없으면 Wave를 `DONE`으로 기록하고 종료한다.
8. **종료(Preview)**: 다음 중 하나면 `WAITING_FOR_PREVIEW`로 기록하고 종료한다. 사람이 확인하기 전에는 다음 Wave로 넘어가지 않는다.
   - Wave의 모든 Task가 `DONE`이고 `Preview Checkpoint`가 있다.
   - 다음 READY Task가 `MANUAL` Category다(사람이 해야 하는 확인이므로 자동으로 `DONE`을 쓰지 않는다).

### 작업 트리 허용 범위

Task 하나가 끝나도 Commit하지 않으므로 다음 Task의 점검 때 작업 트리에는 이전 변경이 남아 있다. 다음만 허용하고 이 밖의 변경·untracked 파일이 있으면 `BLOCKED_DIRTY_TREE`다.

- `WAVE_STATE`에서 `DONE`인 Task의 `files`와 현재 `IN_PROGRESS` Task의 Expected Files
- `TASKS/WAVE_STATE.json`

Wave를 시작할 때(첫 Task) 작업 트리는 완전히 깨끗하거나 위 범위 안이어야 한다. 사용자가 Task별로 직접 Commit하고 싶으면 Task 사이에 Commit한 뒤 `/run-wave resume`을 쓸 수 있다.

## `/run-wave status`

`WAVE_PLAN`·`WAVE_STATE`를 읽어 Wave별(상태, 완료 Task 수/전체, Preview Checkpoint)과 Task별(Wave, 상태, 막힌 이유)을 표로 보여주고, 다음에 실행될 READY Task와 필요한 사람의 조치를 한 줄로 알려준다. 아무것도 수정하지 않는다. `WAVE_STATE`에 기록되지 않은 Task는 `PENDING`이다.

## `/run-wave resume`

- 상태가 `WAITING_FOR_PREVIEW`인 Wave가 있으면: Checkpoint(대상 Screen의 Desktop 1440·Mobile 390 Preview)를 사람이 확인했는지 **사용자에게 묻는다.** 사용자가 확인했다고 답한 경우에만 `preview_confirmed`를 기록하고 Wave를 `DONE`으로 바꾼 뒤 종료한다. 다음 Wave는 자동으로 시작하지 않으며 사용자가 `/run-wave W04`로 시작한다. 확인하지 않았으면 그대로 둔다. 사람의 확인을 대신 판정하지 않는다.
- `IN_PROGRESS` Task가 있으면(중단된 실행): 그 Task를 이어서 구현한다. 작업 트리 변경은 그 Task의 Expected Files 안에 있어야 한다.
- `BLOCKED`·`FAILED` Task가 있으면: 사유를 보여주고 사용자가 해결했다고 하면 `PENDING`으로 돌린 뒤 `/run-wave <Wave>` 흐름으로 이어간다. 사유를 임의로 지우지 않는다.
- 중단된 Wave가 없으면 할 일이 없다고 알린다.

## `/run-wave dry-run W03`

읽기만 한다. 아무 파일도 수정하지 않으며 `WAVE_STATE`도 만들지 않는다.

1. `WAVE_PLAN`과 `WAVE_STATE`(없으면 모두 `PENDING`)를 읽는다.
2. 실행하면 처리될 Task를 순서대로 나열한다(각 Task의 선행 조건 충족 여부, 이전 Wave 미완료 때문에 시작할 수 없는지).
3. 첫 READY Task에 대해서만 prepare-task 판정을 읽기 전용으로 낸다(`READY_TO_IMPLEMENT` 또는 `BLOCKED_*`와 이유).
4. 이 Wave가 `Preview Checkpoint`로 끝나는지 알린다.

## 공통 금지

- 자동 Branch 생성·전환, 자동 Commit·Push, 자동 PR, 자동 Merge, merge queue를 만들거나 실행하지 않는다. destructive Git 명령(`reset`, `checkout --`, `clean`, `stash`, force push)도 쓰지 않는다.
- `WAVE_PLAN`, `TASKS/00_TASK_LIST.md`, `TASKS/TASK-*.md`를 수정하지 않는다. Wave 구성이나 Task 범위를 바꿔야 하면 보고하고 사람이 고치게 한다.
- `WAVE_STATE.json` 외의 `TASKS/` 파일을 갱신하지 않으며, `python scripts/audit_tasks.py`·`gen_task_details.py`를 실행하지 않는다(문서를 다시 쓴다).
- AWS·EC2, ORM, EXCLUDED 기능, Secret 하드코딩, 환경변수 값 출력, 브라우저 Supabase 클라이언트를 만들지 않는다.
- Playwright는 Chromium만, Page Owner 또는 E2E Task에서만 실행한다. spec이 없으면 실행했다고 쓰지 않는다.
- 사람의 Preview·수동 확인을 대신 판정하거나 완료로 기록하지 않는다.

## 종료 보고

실행이 끝나면(어떤 이유로든) 다음을 보고한다.

- 종료 사유: `DONE`, `WAITING_FOR_PREVIEW`, `BLOCKED`(판정과 이유), `FAILED`(실패한 검증)
- 이번 실행에서 `DONE`이 된 Task와 변경 파일, 실행한 검증과 결과
- 남은 Task와 다음에 사람이 할 일(Preview 확인, 환경변수 등록, 변경 Commit)
- 변경이 Commit되지 않은 채 작업 트리에 남아 있다는 사실
