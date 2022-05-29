from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from app.api.v1.auth.mail import send_verification_email
from app.api.v1.auth.models import Token
from app.api.v1.auth.oauth import get_current_active_user, authenticate_user
from app.api.v1.users.models import UserRegister, User
from app.core.config import settings
from app.core.security import get_password_hash, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register")
async def register(user_register: UserRegister):
    user = await User.by_email(user_register.email)
    if user is not None:
        raise HTTPException(status_code=409, detail="An user with that email already exists")
    user = User(
        first_name=user_register.first_name,
        last_name=user_register.last_name,
        email=user_register.email,
        hashed_password=get_password_hash(user_register.password)
    )
    await user.insert()
    await send_verification_email(user)
    return JSONResponse(status_code=201, content="User registered")


# todo
@router.get("/verify")
async def verify(token: str = Depends(get_current_active_user)):
    return JSONResponse(status_code=200, content="User verified")


@router.post("/jwt/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
