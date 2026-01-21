from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.todo import User
from ..schemas.user import UserResponse

router = APIRouter(prefix="/user", tags=["Users"])

# Reusable DB dependency
db_dependency: Annotated[Session, Depends(get_db)]


# GET all users
@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def list_users(db: db_dependency):
    users = db.query(User).all()
    return users


# def check_mail(email: str):
#     for user in Createuser:
#         if user["email"] == email:
#             return False
#     return True


# @router.post("/createuser")
# async def create_user(new_user: User):

#     if not check_mail(new_user.email):
#         return {"error": "This email is already used"}

#     usr = new_user.dict()
#     Createuser.append(usr)

#     return {"message": "Successfully created user", "user": usr}


# @router.put("/update-user/{user_id}")
# async def updateUser(user_id: int, updtaeDetails: User):
#     for usr in Createuser:
#         if usr["id"] == user_id:

#             usr["id"] == updtaeDetails.id
#             usr["username"] = updtaeDetails.username
#             usr["email"] = updtaeDetails.email
#             usr["password"] = updtaeDetails.password
#             usr["is_active"] = updtaeDetails.is_active
#             return {"message": "Successfully update!!", "UpdateUser": usr}

#     return {"message": "Faild Unsuccessfully update!! "}


# @router.delete("/delete/{user_id}")
# async def delete_user(user_id: int):
#     for i, usr in enumerate(Createuser):
#         if usr["id"] == user_id:
#             Createuser.pop(i)
#             return {"message": "Successfully deleted user!"}

#     return {"message": "Failed! User not found"}
