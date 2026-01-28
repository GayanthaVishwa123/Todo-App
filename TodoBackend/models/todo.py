from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from ..auth.passwordAuth import hash_password
from ..core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)


class Task(Base):
    __tablename__ = "todos"

    # Defining the columns
    id = Column(Integer, primary_key=True, index=True)
    taskname = Column(String, index=True)
    task_introduction = Column(String, index=True)
    start_datetime = Column(DateTime, nullable=True)
    complete_datetime = Column(DateTime, nullable=True)
    complete_status = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
