from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_URL = "sqlite:///./todo.db"

create = create_engine(SQLALCHEMY_URL, connect_args={"check_same_thred": False})

sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=Engine)
base = declarative_base()
