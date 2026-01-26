from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.todo import Task
from ..schemas.task import CreatTask, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])

db_dependency = Annotated[Session, Depends(get_db)]
from fastapi import HTTPException, status


@router.get("/", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
async def list_tasks(db: Session = Depends(get_db)):
    try:
        tasks = db.query(Task).all()  # Query all tasks from the database
        if not tasks:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No tasks found"
            )
        return tasks
    except Exception as e:
        # Catch any general exception and raise HTTP 500 (Internal Server Error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


# def idcreate(new_task_id: int = None):
#     if new_task_id is None:
#         if len(tasks) == 0:
#             return 1
#         new_task_id = len(tasks) + 1
#     return new_task_id


@router.post(
    "/create", response_model=TaskResponse, status_code=status.HTTP_201_CREATED
)
async def create_tasks(db: Session, tasks: CreatTask):
    try:
        new_task = Task(**tasks.dict())
        db.commit()
        db.refresh(new_task)
        return new_task

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {str(e)}",
        )


@router.put("/update/{update_id}")
async def update_task(db: db_dependency, update_id: int, updateDetails: CreatTask):
    try:
        # Find task
        task = db.query(Task).filter(Task.id == update_id).first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )

        # Update fields
        task.taskname = updateDetails.taskname
        task.task_introduction = updateDetails.task_introduction
        task.start_datetime = updateDetails.start_datetime
        task.complete_datetime = updateDetails.complete_datetime
        task.complete_status = updateDetails.complete_status

        db.commit()
        db.refresh(task)

        return task

    except Exception as e:
        db.rollback()  # Important if error happens
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Update failed: {str(e)}",
        )

    # for task in tasks:
    #     if task["id"] == update_id:

    #         task["title"] = updateDetails.title
    #         task["task_introduction"] = updateDetails.task_introduction
    #         task["complete_status"] = updateDetails.complete_status
    #         task["start_datetime"] = updateDetails.start_datetime
    #         task["complete_datetime"] = updateDetails.complete_datetime

    #         return {"message": "Task updated successfully", "task": task}

    # return {"error": "Task not found"}


@router.delete("/delete/{task_id}")
async def delete_task(db: db_dependency, task_id: int):
    try:
        task = db.query(Task).filter(Task.id == task_id).first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )

        db.delete(task)
        db.commit()

        return {"message": "Task deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Delete failed: {str(e)}",
        )
