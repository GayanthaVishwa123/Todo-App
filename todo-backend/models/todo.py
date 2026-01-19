from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class Taskclass(BaseModel):

    id: Optional[int] = None
    title: str
    task_introduction: str
    complete_status: bool
    start_datetime: str
    complete_datetime: str


class CreateUser(BaseModel):
    id: Optional[int] = None
    username: str = Field(..., min_length=4)
    email: EmailStr
    password: str = Field(..., min_length=8)
    is_active: Optional[bool] = False
