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
        orm_mode = True  # This is required for SQLAlchemy ORM objects


class UpdateUser(BaseModel):
    firstname: str
    lastname: str
    username: str
