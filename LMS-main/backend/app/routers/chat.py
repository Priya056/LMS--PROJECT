from fastapi import APIRouter, Depends, HTTPException
from openai import OpenAI
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.config import get_settings
from app.context_builder import build_agent_message, load_fraylon_mentor_system_prompt
from app.database import get_db
from app.deps import get_current_user
from app.models import ChatMessage, Problem, Submission, User
from app.schemas import ChatMessageOut, ChatRequest, ChatResponse

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(
    body: ChatRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    s = get_settings()
    if not s.openai_api_key:
        raise HTTPException(
            status_code=503,
            detail="OPENAI_API_KEY is not configured on the server. Set it to enable Fraylon Mentor.",
        )

    p = db.query(Problem).options(joinedload(Problem.course)).filter(Problem.id == body.problem_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Problem not found")

    latest = (
        db.query(Submission)
        .filter(Submission.user_id == user.id, Submission.problem_id == p.id)
        .order_by(Submission.created_at.desc())
        .first()
    )

    user_msg = ChatMessage(user_id=user.id, problem_id=p.id, role="user", content=body.message)
    db.add(user_msg)
    db.commit()

    system_prompt = load_fraylon_mentor_system_prompt()
    contextual = build_agent_message(
        db,
        user,
        p,
        body.message,
        student_code=body.student_code,
        latest_submission=latest,
    )

    client = OpenAI(api_key=s.openai_api_key)
    completion = client.chat.completions.create(
        model=s.openai_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": contextual},
        ],
        temperature=0.7,
    )
    reply = completion.choices[0].message.content or ""

    asst_msg = ChatMessage(user_id=user.id, problem_id=p.id, role="assistant", content=reply)
    db.add(asst_msg)
    db.commit()

    return ChatResponse(reply=reply)


@router.get("/problems/{problem_id}/chat-history", response_model=list[ChatMessageOut])
def chat_history(
    problem_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    p = db.query(Problem).filter(Problem.id == problem_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Problem not found")
    rows = (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == user.id, ChatMessage.problem_id == problem_id)
        .order_by(ChatMessage.created_at.asc())
        .limit(100)
        .all()
    )
    return rows
