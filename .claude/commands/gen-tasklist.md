---
description: 입력 검증 후 TASKS/00_TASK_LIST.md(요약·추적표·Task List 16열)를 생성하고 감사한다
argument-hint: "[추가 지시]"
---

`jobfit-project-pipeline` Skill의 규칙을 따라 `TASKS/00_TASK_LIST.md`를 생성한다. 추가 지시: $ARGUMENTS

공통 규칙
- `jobfit-project-pipeline` Skill을 사용한다.
- 문서를 기억에 의존하지 않고 실제 파일을 읽는다(입력 문서, `package.json`, `src/app` 파일 트리).
- 구현 코드를 만들지 않는다(문서만 작성).
- Task Audit 실패를 무시하지 않는다. 실패하면 완료로 보고하지 않는다.

1. `python scripts/validate_inputs.py`를 실행한다. 실패하면 오류를 보고하고 Task List를 만들지 않는다.
2. Skill의 입력 파일을 읽는다. `src/app` 실제 파일 트리와 `package.json`도 확인한다.
3. `TASKS/` 폴더가 없으면 만들고 `TASKS/00_TASK_LIST.md` 하나만 작성한다(구현 코드·Branch·Commit·Issue 금지). 문서 구성은 Skill의 "00_TASK_LIST.md 형식"을 따른다.
   - 상단 요약: Task 총 개수, Category별 수, Requirement 수
   - Task List 표는 16열(Seq~Priority) 형식을 그대로 사용한다
   - Requirement 추적표에는 PROJECT_SCOPE의 모든 Requirement를 IMPLEMENT/EXCLUDED로 기록하고, EXCLUDED는 NON_IMPLEMENTATION 표에 근거와 후속 방향을 적는다
4. Screen마다 Page Owner를 정확히 하나 만들고, 같은 Screen의 Component·API·Data Task에 의존하게 한다. Page Owner AC에는 Section 순서·Section별 데이터 출처·최소 콘텐츠 수·반응형 밀도·Placeholder 금지·완성형 Empty State를 넣는다.
5. `src/app/page.tsx` Owner, DB 4개 테이블(스키마·RLS·접근 함수 분리), 정적 데이터, LOGIC 단위 테스트, Playwright Chromium E2E(2~3개), CI, Vercel 수동 배포 점검 Task를 Skill 규칙대로 포함한다. 금지 Task(자동 Merge·EC2·AWS·로그인·관리자·결제)는 만들지 않는다.
6. 작성 후 `python scripts/audit_tasks.py`를 실행한다. 오류가 있으면 문서를 고쳐 통과할 때까지 반복한다. 빠진 Requirement ID가 있으면 완료로 보고하지 않는다.
7. 마지막에 Task 수, Category별 개수, IMPLEMENT/EXCLUDED 개수, 감사 결과를 요약한다.
