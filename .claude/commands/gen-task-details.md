---
description: Task List의 구현 Task를 TASKS/TASK-<ID>.md 상세 파일로 모두 변환하고 audit_tasks.py를 실행한다
argument-hint: "[Task ID …] (비우면 전체)"
---

`jobfit-project-pipeline` Skill의 규칙을 따라 Task 상세 파일을 생성한다. 대상: $ARGUMENTS (비우면 전체)

공통 규칙
- `jobfit-project-pipeline` Skill을 사용한다.
- 실제 파일을 읽는다(`TASKS/00_TASK_LIST.md`, 근거 문서, 생성된 `TASKS/TASK-*.md`).
- 구현 코드를 만들지 않는다(문서만 작성).
- Task Audit 실패를 무시하지 않는다. 실패하면 완료로 보고하지 않는다.

1. `TASKS/00_TASK_LIST.md`가 없으면 `/gen-tasklist`를 먼저 실행하라고 안내하고 중단한다.
2. `python scripts/gen_task_details.py`(대상 지정 시 `--only <ID …>`)를 실행한다. 스크립트가 구현 Task ID를 Seq 순서로 읽고 중복 ID·빈 필수 열·존재하지 않는 Depends On을 먼저 검사한다. 실패하면 파일을 만들지 않으므로 `00_TASK_LIST.md`를 고친 뒤 다시 실행한다.
3. 각 구현 Task는 `TASKS/TASK-<ID>.md`로 생성하거나 갱신한다. 같은 ID 파일이 있으면 덮어쓰며 중복 파일을 만들지 않는다. EXCLUDED 행은 파일을 만들지 않는다.
4. 생성된 파일을 읽어 Context·Project Scope·Design Ref·Test Cases가 근거 문서(`06_SRS_UIUX_REVISED.md`, `PROJECT_SCOPE.md`, `UI_CONTRACT.md`, `D-001/DESIGN.md`)와 어긋나지 않는지 확인하고, 보완이 필요하면 `scripts/gen_task_details.py`의 매핑을 고쳐 다시 생성한다. Task List 값은 상세 파일에서 바꾸지 않는다.
5. 구현 코드·Branch·Commit을 만들지 않는다. 구현·테스트가 끝났다고 기록하지 않는다.
6. 생성 후 Task List 구현 ID와 `TASKS/TASK-*.md` 파일명을 1:1로 대조한다.
7. 마지막에 `python scripts/audit_tasks.py`를 실행한다. 실패하면 완료로 보고하지 않고 원인을 고쳐 통과할 때까지 반복한다.
