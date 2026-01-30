from enum import Enum as PyEnum

from sqlalchemy import Boolean, Column, Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..core.database import Base


class Priority(PyEnum):
    Low = "Low"
    Medium = "Medium"
    High = "High"


class TaskStatus(PyEnum):
    Active = "Active"
    Completed = "Completed"
    Pending = "Pending"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    # Relationship to tasks
    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    deadline = Column(Date)
    priority = Column(Enum(Priority), default=Priority.Medium)
    comments = Column(String, nullable=True)
    status = Column(
        Enum(TaskStatus), default=TaskStatus.Active
    )  # False = Active, True = Completed
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship back to user
    owner = relationship("User", back_populates="tasks")
