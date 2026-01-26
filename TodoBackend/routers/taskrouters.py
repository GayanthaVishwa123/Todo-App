from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.todo import Task
from ..schemas.task import CreatTask, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
async def list_tasks(db: Session = Depends(get_db)):
    try:
        tasks = db.query(Task).all()  # Query all tasks
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
async def create_tasks(db: Session = Depends(get_db), task: CreatTask = None):
    try:
        new_task = Task(**task.dict())
        db.add(new_task)  # <-- Add to session
        db.commit()
        db.refresh(new_task)
        return new_task
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@router.put("/update/{update_id}", response_model=TaskResponse)
async def update_task(
    db: Session = Depends(get_db),
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
async def delete_task(db: Session = Depends(get_db), task_id: int = None):
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
