from datetime import date

from fastapi_users import models


class User(models.BaseUser):
    first_name: str
    last_name: str
    birth_date: date
    role: str

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "jdoe@x.edu.ng",
                "birth_date": "08/08/1990",
                "role": "admin",
            }
        }


class UserCreate(models.BaseUserCreate):
    first_name: str
    last_name: str
    birth_date: date
    role: str


class UserUpdate(User, models.BaseUserUpdate):
    first_name: str
    last_name: str
    birth_date: date
    role: str


class UserDB(User, models.BaseUserDB):
    pass
