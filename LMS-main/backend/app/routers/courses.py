from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path

from app.database import get_db
from app.deps import get_current_user
from app.models import Course, Problem, User
from app.schemas import CourseOut, ProblemSummary, LectureOut

router = APIRouter(prefix="/api/courses", tags=["courses"])


@router.get("", response_model=list[CourseOut])
def list_courses(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Course).order_by(Course.id).all()


@router.get("/{slug}/problems", response_model=list[ProblemSummary])
def course_problems(slug: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    course = db.query(Course).filter(Course.slug == slug).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return (
        db.query(Problem)
        .filter(Problem.course_id == course.id)
        .order_by(Problem.sort_order, Problem.id)
        .all()
    )


@router.get("/{slug}/lectures", response_model=list[LectureOut])
def course_lectures(slug: str, _: User = Depends(get_current_user)):
    content_dir = Path(__file__).parent.parent.parent.parent / "content" / slug
    if not content_dir.exists():
        raise HTTPException(status_code=404, detail="Course content not found")
    
    lectures = []
    for lecture_dir in sorted(content_dir.iterdir()):
        if lecture_dir.is_dir() and lecture_dir.name.startswith("lecture_"):
            try:
                number = int(lecture_dir.name.split("_")[1])
                notes_file = lecture_dir / "notes.md"
                if notes_file.exists():
                    content = notes_file.read_text(encoding="utf-8")
                    # Extract title from first line
                    lines = content.split("\n", 1)
                    title = lines[0].strip("# ").strip() if lines[0].startswith("#") else f"Lecture {number}"
                    lectures.append(LectureOut(number=number, title=title, content=content))
            except (ValueError, IndexError):
                continue
    return sorted(lectures, key=lambda l: l.number)
