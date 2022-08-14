from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import EmailStr
from starlette import status

from app.api.v1.auth.models import TokenData
from app.api.v1.users.models import User
from app.core.config import settings
from app.core.security import ALGORITHM, verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/jwt/login")


async def authenticate_user(email: EmailStr, password: str):
    user = await User.find_one(User.email == email)
    password = verify_password(password, user.hashed_password)
    if not user or not password:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user


async def update_password(user: User, password: str):
    user.hashed_password = verify_password(password, user.hashed_password)
    await user.save()


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])
        email: EmailStr = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await User.find_one(User.email == EmailStr(token_data.email))
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(user: User = Depends(get_current_user)):
    if user.is_active is False:
        raise HTTPException(status_code=403, detail="Inactive user")
    return user


async def get_current_verified_user(user: User = Depends(get_current_active_user)):
    if user.is_verified is False:
        raise HTTPException(status_code=403, detail="Unverified user")
    return user


async def get_current_admin(user: User = Depends(get_current_user)):
    if "admin" not in user.role:
        raise HTTPException(status_code=401, detail="Unauthorized user")
    return user
