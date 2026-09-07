from fastapi import FastAPI
from fastapi.responses import JSONResponse

from routes.user import router as user_router

from exceptions.user import UserNotFoundError


app = FastAPI(
    title="User API",
    version="1.0.0"
)

@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )

app.include_router(user_router)