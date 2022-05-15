from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.auth.routers import router as AuthRouter
from .api.v1.users.models import User
from .api.v1.users.routers import router as UsersRouter
from .core.config import settings, db

app = FastAPI(
    title=settings.APP_NAME
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    await init_beanie(
        database=db,
        document_models=[
            User,
        ],
    )


app.include_router(AuthRouter, prefix=settings.API_V1_STR)
app.include_router(UsersRouter, prefix=settings.API_V1_STR)
