from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    name: str = Field(min_length=1, max_length=200)


class LoginBody(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)


class UserOut(BaseModel):
    id: int
    email: str
    name: str

    model_config = {"from_attributes": True}


class CourseOut(BaseModel):
    id: int
    slug: str
    title: str
    description: str

    model_config = {"from_attributes": True}


class ProblemSummary(BaseModel):
    id: int
    slug: str
    title: str
    week_label: str
    sort_order: int

    model_config = {"from_attributes": True}


class ProblemOut(BaseModel):
    id: int
    course_slug: str
    slug: str
    title: str
    description: str
    check50_slug: str
    week_label: str
    sort_order: int

class LectureOut(BaseModel):
    number: int
    title: str
    content: str

class SubmissionCreate(BaseModel):
    code: str


class SubmissionOut(BaseModel):
    id: int
    problem_id: int
    code: str
    output: str
    passed: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatRequest(BaseModel):
    problem_id: int
    message: str
    student_code: str | None = None


class ChatResponse(BaseModel):
    reply: str


class ChatMessageOut(BaseModel):
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}
