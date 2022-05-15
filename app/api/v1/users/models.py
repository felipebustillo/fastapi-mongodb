from datetime import datetime

from beanie import Document
from pydantic import EmailStr, BaseModel


class User(Document):
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str
    is_active = True
    is_verified = False
    role = 'user'
    last_login: datetime
    created = datetime.utcnow()
    updated = datetime.utcnow()


class UserCreate(BaseModel):
    email: EmailStr
    password: str
