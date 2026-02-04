from datetime import datetime
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.todo import Task
from ..routers.userrouters import protected_route
from ..schemas.task import CreateTask, TaskResponse, TaskStatus

router = APIRouter(prefix="/tasks", tags=["Tasks"])

db_dependancy = Annotated[Session, Depends(get_db)]


# current_user: dict = Depends(protected_route)
# Task.user_id == current_user["user_id"]
@router.get("/", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
async def list_tasks(db: db_dependancy, current_user: dict = Depends(protected_route)):
    try:
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
            )

        tasks = db.query(Task).filter(Task.user_id == current_user["user_id"]).all()
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
async def create_task(
    task: CreateTask,
    db: db_dependancy,
    current_user: dict = Depends(protected_route),
):
    try:
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
            )

        # Create a new Task object using the task data
        new_task = Task(**task.dict())
        new_task.user_id = current_user["user_id"]

        # Add the new task to the database session
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@router.put("/update/{task_id}", response_model=TaskResponse)
async def update_task(
    db: db_dependancy,
    task_id: int,
    task: CreateTask,
    current_user: dict = Depends(protected_route),
):
    try:
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
            )

        existing_task = (
            db.query(Task)
            .filter(Task.id == task_id, Task.user_id == current_user["user_id"])
            .first()
        )
        if not existing_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )

        # Update fields
        existing_task.title = task.title
        existing_task.deadline = task.deadline
        existing_task.priority = task.priority
        existing_task.comments = task.comments

        db.commit()
        db.refresh(existing_task)

        return existing_task

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Update failed: {str(e)}",
        )


@router.delete("/delete/{task_id}")
async def delete_task(
    db: db_dependancy,
    task_id: int,
    current_user: dict = Depends(protected_route),
):
    try:
        task = (
            db.query(Task)
            .filter(Task.id == task_id and Task.user_id == current_user)
            .first()
        )
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


@router.put("/complete/{task_id}", response_model=TaskResponse)
async def complete_task(
    task_id: int, db: db_dependancy, current_user: dict = Depends(protected_route)
):
    try:
        task = (
            db.query(Task)
            .filter(Task.id == task_id, Task.user_id == current_user["user_id"])
            .first()
        )

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )

        task.status = TaskStatus.Completed

        db.commit()
        db.refresh(task)

        return task

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@router.put("/Undocomplete/{task_id}", response_model=TaskResponse)
async def complete_task(
    task_id: int, db: db_dependancy, current_user: dict = Depends(protected_route)
):
    try:
        task = (
            db.query(Task)
            .filter(Task.id == task_id, Task.user_id == current_user["user_id"])
            .first()
        )

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )

        task.status = TaskStatus.Active

        db.commit()
        db.refresh(task)

        return task

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )
