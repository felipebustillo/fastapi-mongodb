from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from starlette.responses import JSONResponse

from app.api.v1.auth.models import Token
from app.api.v1.auth.oauth import authenticate_user
from app.api.v1.users.models import User, UserRegister
from app.core.config import settings
from app.core.security import get_password_hash, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


# TODO
@router.post("/register")
async def register(user_register: UserRegister):
    user = await User.find_one(User.email == user_register.email)
    if user:
        raise HTTPException(status_code=409, detail="An user with that email already exists")
    user = User(
        first_name=user_register.first_name,
        last_name=user_register.last_name,
        email=user_register.email,
        hashed_password=get_password_hash(user_register.password),
        role=["user"]
    )
    await user.create()
    # await send_verification_email(user)
    return JSONResponse(status_code=201, content="User registered")


@router.post("/jwt/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    await authenticate_user(EmailStr(form_data.username), form_data.password)
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    user = await User.find_one(User.email == form_data.username)
    user.last_login = datetime.utcnow()
    await user.save()
    return {"access_token": access_token, "token_type": "bearer"}


# TODO
@router.post("/password_reset/{user_email}")
async def password_reset(user_email: EmailStr):
    user = await User.find_one(User.email == user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # await send_password_reset_email(email)
    return JSONResponse(status_code=200, content="Password reset email sent")
