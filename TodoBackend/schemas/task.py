from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# Enum to represent task priority (Low, Medium, High)
class Priority(str, Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"


class TaskStatus(str, Enum):
    Active = "Active"
    Completed = "Completed"
    Pending = "Pending"


# Pydantic model for creating a task (request body)
class CreateTask(BaseModel):
    title: str = Field(..., max_length=255)
    deadline: Optional[date]
    priority: Optional[Priority] = Priority.Medium
    comments: Optional[str] = None
    comments: str = Field(..., max_length=500)

    class Config:
        # Convert data models to attributes and not keys
        from_attributes = True


# Pydantic model for responding with task details (response body)
class TaskResponse(BaseModel):
    id: int
<<<<<<< HEAD
<<<<<<< HEAD

    taskname: str
    task_introduction: str
    start_datetime: datetime
    complete_status: bool
=======
=======
>>>>>>> dev
    title: str
    deadline: Optional[date]
    priority: Priority
    comments: Optional[str]
    status: Optional[TaskStatus] = TaskStatus.Active
<<<<<<< HEAD
>>>>>>> dev
=======
>>>>>>> dev
    user_id: int

    class Config:
        from_attributes = True
