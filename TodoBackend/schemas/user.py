from pydantic import BaseModel, Field


class CreateRequestUser(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: str
    password: str = Field(..., min_length=6, max_length=72)


class UserResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    email: str
    token: str

    class Config:
        from_attributes = True


class UpdateUser(BaseModel):
    firstname: str
    lastname: str
    username: str


class AllusersResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    username: str
    email: str
