from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import EmailStr, BaseModel


class User(Document):
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    password: str
    is_active = True
    is_verified = False
    role = "user"
    last_login: Optional[datetime]
    created = datetime.utcnow()
    updated = datetime.utcnow()

    @classmethod
    async def by_email(cls, email: EmailStr):
        return await cls.find_one(cls.email == email)


class UserRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
