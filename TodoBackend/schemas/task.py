from typing import Optional

from pydantic import BaseModel


class CreatTask(BaseModel):
    taskname = str
    task_introduction = str
    start_datetime = str
    complete_datetime = str
