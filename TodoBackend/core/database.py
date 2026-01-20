from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL
SQLALCHEMY_URL = "sqlite:///./todo.db"

# Creating the engine, using SQLite. The `check_same_thread` argument ensures SQLite works in multiple threads.
engine = create_engine(SQLALCHEMY_URL, connect_args={"check_same_thread": False})

# Creating a sessionmaker for managing sessions
sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Base class for models
Base = declarative_base()
