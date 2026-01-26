from typing import Optional

from pydantic import BaseModel


class CreatTask(BaseModel):
    taskname: str
    task_introduction: str
    start_datetime: str
    complete_datetime: str


class TaskResponse(BaseModel):
    id: int
    taskname: str
    task_introduction: str
    complete_status: str

    class Config:
        from_attributes = True
