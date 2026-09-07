from fastapi import FastAPI

from routes.user import router as user_router


app = FastAPI(
    title="User API",
    version="1.0.0"
)


app.include_router(user_router)