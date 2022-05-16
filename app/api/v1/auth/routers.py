from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Body, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import EmailStr

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
    if (user_register):
        raise HTTPException(
            status_code=409,
            detail="An user with that email already exists"
        )
    user = User()
    user.hashed_password = get_password_hash(user_register.password)
    await user.insert()
    return Response(status_code=200)


@router.post("/login")
async def login(user: UserLogin):
    return user