import uvicorn
from fastapi import FastAPI

from api.v1.users.routers import get_users_router
from core.config import settings

app = FastAPI()

# Add FastAPI Users router
app.include_router(get_users_router())

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
