from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas.task import CreaetTask
from ..schemas.user import CreateRequestUser

router = APIRouter(prefix="/tasks", tags=["Tasks"])

db_dependency: Annotated[Session, Depends(get_db)]


# @router.get("/")
# async def list():
#     return tasks


# def idcreate(new_task_id: int = None):
#     if new_task_id is None:
#         if len(tasks) == 0:
#             return 1
#         new_task_id = len(tasks) + 1
#     return new_task_id


# @router.post("/create")
# async def create_tasks(newTasks: Task):
#     newTasks.id = idcreate(newTasks.id)
#     tasks.append(newTasks.dict())
#     return {"message": "Task created successfully", "task": tasks}


# @router.put("/update/{update_id}")
# async def update_task(update_id: int, updateDetails: Task):

#     for task in tasks:
#         if task["id"] == update_id:

#             task["title"] = updateDetails.title
#             task["task_introduction"] = updateDetails.task_introduction
#             task["complete_status"] = updateDetails.complete_status
#             task["start_datetime"] = updateDetails.start_datetime
#             task["complete_datetime"] = updateDetails.complete_datetime

#             return {"message": "Task updated successfully", "task": task}

#     return {"error": "Task not found"}


# @router.delete("/delete/{task_id}")
# async def delete_task(task_id: int):
#     for i, task in enumerate(tasks):
#         if task.get("id") == task_id:
#             tasks.pop(i)
#             return {"message": "Task deleted successfully", "tasks": tasks}
