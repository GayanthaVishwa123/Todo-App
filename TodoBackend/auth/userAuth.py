from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..auth.passwordAuth import password_verified
from ..core.database import get_db
from ..models.todo import User

# Dependency to get DB session
db_dependency = Annotated[Session, Depends(get_db)]

# Secret key and algorithm for JWT token creation
SECRET_KEY = "df08a3baaa2ee64e49006c4a33c848fa6cc2176e960a1ad21a1e1cac66c53499"
ALGORITHM = "HS256"


class AccessToken(BaseModel):
    access_token: str
    token_type: str


def userAuthenticate(user_name: str, password: str, db: db_dependency):

    userdetails = db.query(User).filter(User.username == user_name).first()

    # Check if the user exists
    if not userdetails:
        raise HTTPException(status_code=404, detail="User not found")

    if not password_verified(password, userdetails.has_password):
        raise HTTPException(status_code=400, detail="Invalid password")

    # Return the user object if authentication is successful
    return userdetails


def create_token(username: str, user_id: int, expire_time: timedelta):

    encoded_data = {"sub": username, "id": user_id}

    expiration = datetime.utcnow() + expire_time
    encoded_data.update({"exp": expiration})

    # Create and return the JWT token
    return jwt.encode(encoded_data, SECRET_KEY, algorithm=ALGORITHM)


# Decode the JWT token
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload["sub"]
        user_id: int = payload["id"]
        return {"username": username, "user_id": user_id}
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
