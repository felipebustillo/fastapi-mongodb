from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Body, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.api.v1.auth.mail import send_verification_email
from app.api.v1.auth.models import Token
from app.api.v1.users.models import UserRegister, UserLogin, User
from app.core.config import db, settings
from app.core.security import create_access_token, ALGORITHM, get_password_hash

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register")
async def register(user_register: UserRegister):
    user = await User.by_email(user_register.email)
    if user is not None:
        raise HTTPException(
            status_code=409,
            detail="An user with that email already exists"
        )
    user = User(
        first_name=user_register.first_name,
        last_name=user_register.last_name,
        email=user_register.email,
        password=get_password_hash(user_register.password),
    )
    await user.insert()
    await send_verification_email(user)
    return Response(
        status_code=201,
        content="User created"
    )


@router.post("/verify/{token}")
async def verify(user: UserLogin):
    return user


@router.post("/login")
async def login(user: UserLogin):
    return user