from fastapi_users import models


class User(models.BaseUser):
    first_name: str
    last_name: str

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "jdoe@x.edu.ng",
            }
        }


class UserCreate(models.BaseUserCreate):
    first_name: str
    last_name: str


class UserUpdate(User, models.BaseUserUpdate):
    first_name: str
    last_name: str


class UserDB(User, models.BaseUserDB):
    pass
