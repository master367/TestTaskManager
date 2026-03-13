from datetime import datetime
from typing import Annotated, Optional, Any

from pydantic import BaseModel, ConfigDict, Field, EmailStr, StringConstraints
from pydantic.functional_validators import BeforeValidator

from app.models import TaskStatus

def normalize_email(v: Any) -> Any:
    if isinstance(v, str):
        v = v.strip().lower()
        if not v.isascii():
            raise ValueError("Email must contain only Latin characters (no Cyrillic allowed)")
        return v
    return v

NormalizedEmail = Annotated[EmailStr, BeforeValidator(normalize_email)]
StrippedString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


TaskTitleString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
TaskDescriptionString = Annotated[str, StringConstraints(strip_whitespace=True)]

class TaskCreate(BaseModel):
    title: TaskTitleString
    description: Optional[TaskDescriptionString] = None
    status: TaskStatus = TaskStatus.todo


class TaskUpdate(BaseModel):
    title: Optional[TaskTitleString] = None
    description: Optional[TaskDescriptionString] = None
    status: Optional[TaskStatus] = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: TaskStatus
    user_id: int
    created_at: datetime
    updated_at: datetime


class PaginatedTaskResponse(BaseModel):
    items: list[TaskResponse]
    total: int
    limit: int
    offset: int

class UserCreate(BaseModel):
    email: NormalizedEmail
    password: Annotated[str, StringConstraints(strip_whitespace=True, min_length=6)]
    name: StrippedString


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    name: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
