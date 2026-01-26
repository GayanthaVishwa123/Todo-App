from typing import Optional

from pydantic import BaseModel


class CreatTask(BaseModel):
    taskname: str
    task_introduction: str
    start_datetime: str
    complete_datetime: str


class TaskResponse(BaseModel):
<<<<<<< HEAD

=======
    id: int
>>>>>>> dev
    taskname: str
    task_introduction: str
    complete_status: str

    class Config:
<<<<<<< HEAD
        from_attributes = True  # Pydantic v2
=======
        from_attributes = True
>>>>>>> dev
