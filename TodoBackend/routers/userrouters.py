from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session

from ..auth.passwordAuth import hash_password, password_verified
from ..auth.userAuth import AccessToken, userAuthenticate
from ..core.database import get_db
from ..models.todo import User
from ..schemas.user import CreateRequestUser, UpdateUser, UserResponse

router = APIRouter(prefix="/user", tags=["Users"])


db_dependency = Annotated[Session, Depends(get_db)]


# OAuth2PasswordBearer instance to extract token from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

from TodoBackend.auth.userAuth import (
    AccessToken,
    create_token,
    decode_token,
    userAuthenticate,
)


# GET all users
@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def list_users(db: db_dependency):
    users = db.query(User).all()
    return users


# Post users
@router.post(
    "/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def createUser(db: db_dependency, user: CreateRequestUser):
    try:
        hashed_pw = hash_password(user.password)
        print("Hashed Password:", hashed_pw)

        new_user = User(
            firstname=user.firstname,
            lastname=user.lastname,
            username=user.username,
            email=user.email,
            password=hashed_pw,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"User creation failed: {str(e)}")


# user Update
@router.put(
    "/userUpdate/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def user_update(db: db_dependency, user_id: int, user: UpdateUser):
    try:

        update_user = db.query(User).filter(User.id == user_id).first()

        if not update_user:
            raise HTTPException(status_code=404, detail="User not found")

        update_user.firstname = user.firstname
        update_user.lastname = user.lastname
        update_user.username = user.username

        db.commit()
        db.refresh(update_user)

        return update_user

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating user: {str(e)}")


# user Delete
@router.delete("/userdele/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(db: db_dependency, user_id: int):
    try:

        user_to_delete = db.query(User).filter(User.id == user_id).first()

        if not user_to_delete:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(user_to_delete)
        db.commit()

        return {"message": "User successfully deleted"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting user: {str(e)}")


@router.post("/login", response_model=AccessToken)
async def login_access_token(
    form: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    # Authenticate the user
    user = userAuthenticate(form.username, form.password, db)
    print(user)

    if not isinstance(user, User):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Create access token
    token = create_token(user.username, user.id, timedelta(minutes=20))
    print(token)
    return AccessToken(access_token=token, token_type="bearer")


# Protected route using Bearer token
@router.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    # Decode the token to get the user details
    user_info = decode_token(token)
    return {
        "message": f"Hello {user_info['username']}, you are authorized to view this resource."
    }
