from fastapi import APIRouter
from pydantic import EmailStr

from app.api.v1.users.models import UserRegister, UserLogin

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register")
async def register(user: UserRegister):
    return user


@router.post("/login")
async def login(user: UserLogin):
    return user


@router.post("/forgot-password")
async def forgot_password(email: EmailStr):
    return email
