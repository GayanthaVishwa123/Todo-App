from pydantic import BaseModel


class CreateRequestUser(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: str
    has_password: str


class UserResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    email: str

    class Config:
        from_attributes = True


class updateUser(BaseModel):
    firstname: str
    lastname: str
    username: str
