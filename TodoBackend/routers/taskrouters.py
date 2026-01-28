from datetime import datetime
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.todo import Task
from ..schemas.task import CreatTask, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])

task_array = []

db_dependancy = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
async def list_tasks(db: db_dependancy):
    try:
        tasks = db.query(Task).all()
        if not tasks:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No tasks found"
            )
        return tasks

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@router.post(
    "/create", response_model=TaskResponse, status_code=status.HTTP_201_CREATED
)
async def create_tasks(db: db_dependancy, task: CreatTask = None):

    try:

        new_task = Task(**task.model_dump())
        task_array.append(new_task)

        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        print(task_array)
        return new_task

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@router.put("/update/{update_id}", response_model=TaskResponse)
async def update_task(
    db: db_dependancy,
    update_id: int = None,
    updateDetails: CreatTask = None,
):
    try:
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

        # If you have complete_status in Task model, update it here too
        if hasattr(updateDetails, "complete_status"):
            task.complete_status = updateDetails.complete_status

        db.commit()
        db.refresh(task)
        return task
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Update failed: {str(e)}",
        )


@router.delete("/delete/{task_id}")
async def delete_task(db: db_dependancy, task_id: int = None):
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


@router.put("/completeTask/{task_id}")
async def complete_task(task_id: int, db: db_dependancy):
    try:
        # Fetch the task from the database by task_id
        task = db.query(Task).filter(Task.id == task_id).first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )

        # Mark task as completed and set the completion time
        task.complete_status = True
        task.complete_datetime = datetime.utcnow()

        db.commit()

        db.refresh(task)

        # Return a success message with task completion details
        return {
            "message": "Task completed",
            "task_id": task.id,
            "completed_at": task.complete_datetime,
        }

    except Exception as e:
        # Catch any error that occurs and raise an internal server error with the message
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@router.delete("/removeCompleteTask/{task_id}")
async def remove_complete_task(task_id: int, db: db_dependancy):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return {"message": "Task not found"}

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}
