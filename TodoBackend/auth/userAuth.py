from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..auth.passwordAuth import passwordVeryfied
from ..core.database import get_db
from ..models.todo import User

db_dependency = Annotated[Session, Depends(get_db)]


def userAuthenticate(user_name: str, password: str, db: db_dependency):
    userdetails = db.query(User).filter(User.username == user_name).first()
    if not userdetails:
        return {"error"}
    if not passwordVeryfied(password, userdetails.has_password):
        return {"message": "Erroer"}
    return True




def login_access():