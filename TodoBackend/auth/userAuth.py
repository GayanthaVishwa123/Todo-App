from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..auth.passwordAuth import passwordVeryfied
from ..core.database import get_db
from ..models.todo import User

# Dependency to get DB session
db_dependency = Annotated[Session, Depends(get_db)]

# Secret key and algorithm for JWT token creation
SECRET_KEY = "df08a3baaa2ee64e49006c4a33c848fa6cc2176e960a1ad21a1e1cac66c53499"
ALGORITHM = "HS256"

# OAuth2PasswordBearer instance to extract token from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AccessToken(BaseModel):
    access_token: str
    token_type: str


# Authenticate the user
def userAuthenticate(user_name: str, password: str, db: db_dependency):
    userdetails = db.query(User).filter(User.username == user_name).first()
    if not userdetails:
        return {"error": "User not found"}
    if not passwordVeryfied(
        password, userdetails.has_password
    ):  # Assuming passwordVeryfied is implemented
        return {"message": "Invalid password"}
    return userdetails  # Return user details for token creation


# Create JWT token function
def create_token(username: str, user_id: int, expire_time: timedelta):
    encoded_data = {"sub": username, "id": user_id}
    expire_time = datetime.utcnow() + expire_time
    encoded_data.update({"exp": expire_time})

    # Correct the spelling of 'encode'
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


# Token endpoint for login (OAuth2 Password Flow)
@app.post("/token", response_model=AccessToken)
async def login_access_token(
    form: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    # Authenticate the user
    user = userAuthenticate(form.username, form.password, db)
    if not isinstance(user, User):  # Check if user authentication was successful
        raise HTTPException(status_code=400, detail=user["message"])

    # Create access token
    token = create_token(user.username, user.id, timedelta(minutes=20))
    return AccessToken(access_token=token, token_type="bearer")


# Protected route using Bearer token
@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    # Decode the token to get the user details
    user_info = decode_token(token)
    return {
        "message": f"Hello {user_info['username']}, you are authorized to view this resource."
    }
