from fastapi import FastAPI
from fastapi.responses import JSONResponse

from routes.user import router as user_router

from exceptions.base import AppException


app = FastAPI(
    title="User API",
    version="1.0.0"
)

@app.exception_handler(AppException)
async def user_not_found_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

app.include_router(user_router)