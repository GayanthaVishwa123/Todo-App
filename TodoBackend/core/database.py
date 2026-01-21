from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_URL = "sqlite:///./todo.db"


engine = create_engine(SQLALCHEMY_URL, connect_args={"check_same_thread": False})


sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
