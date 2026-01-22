from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..auth.passwordAuth import passwordVeryfied
from ..core.database import get_db
from ..models.todo import User

db_dependency = Annotated[Session, Depends(get_db)]

SECRET_KEY = "df08a3baaa2ee64e49006c4a33c848fa6cc2176e960a1ad21a1e1cac66c53499"
ALGORITHUM = "HA256"


class AcessToken(BaseModel):
    acsess_token: str
    token_type: str


def userAuthenticate(user_name: str, password: str, db: db_dependency):
    userdetails = db.query(User).filter(User.username == user_name).first()
    if not userdetails:
        return {"error"}
    if not passwordVeryfied(password, userdetails.has_password):
        return {"message": "Erroer"}
    return True


def cretae_token(username: str, user_id: int, expireTime: timedelta):
    enacode = {"sub": username, "id": user_id}
    expiretime = datetime.utcnow() + expireTime
    # enacode['exp']=expiretime
    enacode.update({"exp": expiretime})

    return jwt.enacode(enacode, SECRET_KEY, algorithum=ALGORITHUM)

def login_acsess():
    



def loginaccsess_token(
    form: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = userAuthenticate(form.username, form.password, db)
    if not user:
        return {"mesage"}
    token = cretae_token(user.username, user.id, timedelta(minutes=20))
    return token
