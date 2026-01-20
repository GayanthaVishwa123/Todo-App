from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from ..core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)


class Task(Base):
    __tablename__ = "todos"

    # Defining the columns
    id = Column(Integer, primary_key=True, index=True)
    task_introduction = Column(String, index=True)
    complete_status = Column(Boolean, default=False)
    start_datetime = Column(String)
    complete_datetime = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
