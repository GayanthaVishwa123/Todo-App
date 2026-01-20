from fastapi import APIRouter

# from ..models.todo import User

router = APIRouter(prefix="/user", tags=["Users"])

# Createuser = [
#     {
#         "id": 1,
#         "username": "student01",
#         "email": "student01@gmail.com",
#         "password": "studentpass123",
#     },
#     {
#         "id": 2,
#         "username": "student02",
#         "email": "student02@gmail.com",
#         "password": "studentpass1234",
#     },
# ]


# @router.get("/")
# async def get_user():
#     return {"message": "Successfully see users", "users": Createuser}


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
