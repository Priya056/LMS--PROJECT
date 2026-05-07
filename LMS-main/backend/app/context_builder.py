"""Runtime context injection per agent_prompt.md."""

from pathlib import Path

from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import Problem, Submission, User


def load_fraylon_mentor_system_prompt() -> str:
    """Single source of truth: agent_prompt.md in the academy repository root."""
    root = get_settings().academy_root
    path = root / "agent_prompt.md"
    if not path.is_file():
        raise FileNotFoundError(f"agent_prompt.md not found at {path}")
    md = path.read_text(encoding="utf-8")
    start_key = "You are **Fraylon Mentor**"
    end_key = "## RUNTIME CONTEXT INJECTION"
    start = md.index(start_key)
    end = md.index(end_key)
    return md[start:end].strip()


def list_completed_problem_titles(db: Session, user_id: int) -> list[str]:
    passed = (
        db.query(Problem.title)
        .join(Submission, Submission.problem_id == Problem.id)
        .filter(Submission.user_id == user_id, Submission.passed.is_(True))
        .distinct()
        .all()
    )
    return [row[0] for row in passed]


def build_agent_message(
    db: Session,
    student: User,
    problem: Problem,
    student_message: str,
    *,
    student_code: str | None = None,
    latest_submission: Submission | None = None,
) -> str:
    """Compose the user message with injected session context (matches agent_prompt template)."""
    course_name = problem.course.slug.upper().replace("CS50", "CS50")
    if problem.course.slug == "cs50p":
        course_display = "CS50P"
    elif problem.course.slug == "cs50ai":
        course_display = "CS50AI"
    else:
        course_display = course_name

    past_count = (
        db.query(Submission)
        .filter(Submission.user_id == student.id, Submission.problem_id == problem.id)
        .count()
    )

    completed = list_completed_problem_titles(db, student.id)
    completed_str = ", ".join(completed) if completed else "(none yet)"

    ctx = f"""=== CURRENT SESSION CONTEXT ===

STUDENT: {student.name} (ID: {student.id})
COURSE: {course_display}
CURRENT PROBLEM: {problem.title}

PROBLEM DESCRIPTION:
{problem.description}

CHECK50 SLUG: {problem.check50_slug}
(e.g. cs50/problems/2022/python/indoor)

"""

    code = student_code
    if code is None and latest_submission:
        code = latest_submission.code

    if code:
        ctx += f"""STUDENT'S CURRENT CODE (if any):
```python
{code}
```

"""

    if latest_submission:
        overall = "PASSED" if latest_submission.passed else "FAILED"
        ctx += f"""CHECK50 RESULTS (if student just submitted):
- Overall: {overall}
- Raw output:
{latest_submission.output}

"""

    ctx += f"""STUDENT'S PREVIOUS SUBMISSIONS ON THIS PROBLEM: {past_count}
PROBLEMS COMPLETED SO FAR: {completed_str}

=== END CONTEXT ===

Student message: {student_message}
"""
    return ctx
