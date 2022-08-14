from datetime import datetime
from typing import Optional, List

from beanie import Document
from pydantic import EmailStr, BaseModel


class User(Document):
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str
    is_active = True
    is_verified = False
    role: List[str]
    last_login: Optional[datetime]
    created = datetime.utcnow()
    updated = datetime.utcnow()

    class Collection:
        name = "users"


class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]
    is_active: Optional[bool]
    is_verified: Optional[bool]
    role: Optional[List[str]]
    updated = datetime.utcnow()


class UserRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserUpdateCurrent(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
