import ast

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.database import get_db
from app.deps import get_current_user
from app.models import Problem, Submission, User
from app.schemas import SubmissionCreate, SubmissionOut

router = APIRouter(prefix="/api/problems", tags=["submissions"])


def _demo_check50_output(code: str) -> tuple[bool, str]:
    try:
        ast.parse(code)
    except SyntaxError as e:
        return False, f":( syntax_error\n    {e}\n"
    out = "\n".join(
        [
            ":) local_check passes ast_parse",
            "",
            "Note: This demo LMS only validates Python syntax. Connect the real check50 tool for full tests.",
        ]
    )
    return True, out


@router.post("/{problem_id}/submit", response_model=SubmissionOut)
def submit(
    problem_id: int,
    body: SubmissionCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    p = db.query(Problem).options(joinedload(Problem.course)).filter(Problem.id == problem_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Problem not found")
    passed, output = _demo_check50_output(body.code)
    sub = Submission(
        user_id=user.id,
        problem_id=p.id,
        code=body.code,
        output=output,
        passed=passed,
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub
