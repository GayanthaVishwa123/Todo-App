from fastapi import APIRouter

from ..models.todo import Taskclass

router = APIRouter(prefix="/tasks", tags=["Tasks"])


tasks = [
    {
        "id": 1,
        "title": "Complete Assignment",
        "task_introduction": "Complete the Assignment",
        "complete_status": False,
        "start_datetime": "2026-01-17 08:09:00",
        "complete_datetime": "2026-02-23 02:23:33",
    },
    {
        "id": 2,
        "title": "Complete Practical",
        "task_introduction": "Complete the Practical",
        "complete_status": False,
        "start_datetime": "2026-01-13 12:23:33",
        "complete_datetime": "2026-01-23 02:23:33",
    },
]


@router.get("/")
async def lists():
    return tasks


def idcreate(new_task_id: int = None):
    if new_task_id is None:
        if len(tasks) == 0:
            return 1
        new_task_id = len(tasks) + 1
    return new_task_id


@router.post("/create")
async def create_tasks(newTasks: Taskclass):
    newTasks.id = idcreate(newTasks.id)
    tasks.append(newTasks.dict())
    return {"message": "Task created successfully", "task": tasks}


@router.put("/update/{update_id}")
async def update_task(update_id: int, updateDetails: Taskclass):

    for task in tasks:
        if task["id"] == update_id:

            task["title"] = updateDetails.title
            task["task_introduction"] = updateDetails.task_introduction
            task["complete_status"] = updateDetails.complete_status
            task["start_datetime"] = updateDetails.start_datetime
            task["complete_datetime"] = updateDetails.complete_datetime

            return {"message": "Task updated successfully", "task": task}

    return {"error": "Task not found"}


@router.delete("/delete/{task_id}")
async def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task.get("id") == task_id:
            tasks.pop(i)
            return {"message": "Task deleted successfully", "tasks": tasks}
