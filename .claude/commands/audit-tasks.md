---
description: 입력 문서와 TASKS/00_TASK_LIST.md를 검증한다 (validate_inputs.py + audit_tasks.py)
argument-hint: "[--tasks-dir 경로] [--list 파일명]"
---

Task 문서를 감사한다. 인자: $ARGUMENTS (기본: `TASKS/00_TASK_LIST.md`)

1. `python scripts/validate_inputs.py`를 실행한다.
2. `python scripts/audit_tasks.py $ARGUMENTS`를 실행한다.
3. 결과를 오류·경고로 나눠 보고한다. 각 오류는 Task ID(또는 Requirement ID)와 원인을 함께 적는다.
4. 오류가 있으면 사용자가 요청한 경우에만 Task 문서를 수정하고 다시 실행한다. 감사 통과를 위해 스크립트 검사 기준을 완화하지 않는다.
5. 감사는 문서 일관성만 검증한다. 코드 구현·테스트 통과 여부를 뜻하지 않으므로 그렇게 보고하지 않는다.
