from pydantic import BaseModel


class CreaetTask(BaseModel):
    taskname = str
    task_introduction = str
    complete_status = str
    start_datetime = str
    complete_datetime = str
