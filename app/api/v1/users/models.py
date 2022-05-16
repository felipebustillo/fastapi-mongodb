from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import EmailStr, BaseModel


class User(Document):
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str
    is_active = True
    is_verified = False
    role = "user"
    last_login: Optional[datetime]
    created = datetime.utcnow()
    updated = datetime.utcnow()


class UserRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
