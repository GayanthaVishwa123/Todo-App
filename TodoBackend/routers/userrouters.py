from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session

from ..auth.passwordAuth import hash_password
from ..auth.userAuth import (
    ALGORITHM,
    SECRET_KEY,
    AccessToken,
    create_token,
    get_current_user,
    userAuthenticate,
)
from ..core.database import get_db
from ..models.todo import User
from ..schemas.user import AllusersResponse, CreateRequestUser, UpdateUser, UserResponse

db_dependency = Annotated[Session, Depends(get_db)]

# OAuth2PasswordBearer instance to extract token from Authorization header
router = APIRouter(prefix="/user", tags=["Users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def protected_route(token: str = Depends(oauth2_scheme)):
    # Get user info from the decoded token
    user_info = get_current_user(token)

    # Return a response indicating that the user is authorized
    return user_info
    print(user_info)


# current_user: dict = Depends(protected_route)
# filter((User.id != current_user["user_id"]))
# GET all users
@router.get("/", response_model=list[AllusersResponse], status_code=status.HTTP_200_OK)
async def list_users(db: db_dependency, current_user: dict = Depends(protected_route)):
    # print(current_user)
    users = db.query(User).filter((User.id != current_user["user_id"])).all()
    return users


# Post users
@router.post(
    "/createUser", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def createUser(
    db: db_dependency,
    user: CreateRequestUser,
):
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


# Token endpoint to login and get JWT
@router.post("/login", response_model=AccessToken)
async def login_User(
    form: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    # Authenticate the user
    user = userAuthenticate(form.username, form.password, db)
    if not isinstance(user, User):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    token = create_token(user.username, user.id, timedelta(minutes=10))

    return AccessToken(access_token=token, token_type="bearer")


# User Update
@router.put(
    "/userUpdate/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def user_update(
    db: db_dependency,
    user_id: int,
    user: UpdateUser,
    current_user: dict = Depends(protected_route),
):
    try:
        if not (user_id == current_user["user_id"]):
            raise HTTPException(status_code=404, detail="Could not update")

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


# User Delete
@router.delete("/userdele/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    db: db_dependency, user_id: int, current_user: dict = Depends(protected_route)
):
    try:
        if not (user_id == current_user["user_id"]):
            raise HTTPException(status_code=404, detail="Could not Delete")
        user_to_delete = db.query(User).filter(User.id == user_id).first()

        if not user_to_delete:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(user_to_delete)
        db.commit()

        return {"message": "User successfully deleted"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting user: {str(e)}")


# # Decode the JWT token and get the current user
# def get_current_user(token: str):
#     try:
#         # Decode the JWT token
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         user_id: int = payload.get("id")

#         if username is None or user_id is None:
#             raise HTTPException(
#                 status_code=401, detail="Invalid token: missing user details"
#             )

#         return {"username": username, "user_id": user_id}

#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token has expired")
#     except jwt.JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")


# Protected route to check the user's access
