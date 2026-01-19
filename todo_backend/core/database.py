from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_URL = "sqlite:///./todo.db"

engine = create_engine(SQLALCHEMY_URL, connect_args={"check_same_thred": False})

sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
base = declarative_base()
