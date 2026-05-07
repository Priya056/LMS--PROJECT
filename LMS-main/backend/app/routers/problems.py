from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.deps import get_current_user
from app.models import Problem, User
from app.schemas import ProblemOut

router = APIRouter(prefix="/api/problems", tags=["problems"])


@router.get("/{problem_id}", response_model=ProblemOut)
def get_problem(
    problem_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    p = db.query(Problem).options(joinedload(Problem.course)).filter(Problem.id == problem_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Problem not found")
    return ProblemOut(
        id=p.id,
        course_slug=p.course.slug,
        slug=p.slug,
        title=p.title,
        description=p.description,
        check50_slug=p.check50_slug,
        week_label=p.week_label,
        sort_order=p.sort_order,
    )
