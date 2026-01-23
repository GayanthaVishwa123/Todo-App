from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.todo import User
from ..schemas.user import CreateRequestUser, UserResponse

router = APIRouter(prefix="/user", tags=["Users"])


db_dependency = Annotated[Session, Depends(get_db)]


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
        new_user = User(
            firstname=user.firstname,
            lastname=user.lastname,
            username=user.username,
            email=user.email,
            has_password=user.has_password,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"User creation failed: {str(e)}")


from fastapi import HTTPException


# user Update
@router.put(
    "/userUpdate/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def user_update(db: db_dependency, user_id: int, user: CreateRequestUser):
    try:

        update_user = db.query(User).filter(User.id == user_id).first()

        if not update_user:
            raise HTTPException(status_code=404, detail="User not found")

        update_user.firstname = user.firstname
        update_user.lastname = user.lastname
        update_user.username = user.username
        update_user.email = user.email
        update_user.hashed_password = user.password

        db.commit()
        db.refresh(update_user)

        return update_user

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating user: {str(e)}")


from fastapi import HTTPException


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
