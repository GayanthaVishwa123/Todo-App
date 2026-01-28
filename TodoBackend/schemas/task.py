from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CreatTask(BaseModel):
    taskname: str
    task_introduction: str


class TaskResponse(BaseModel):
    id: int
    taskname: str
    task_introduction: str
    start_datetime: datetime
    complete_status: bool

    class Config:
        from_attributes = True
