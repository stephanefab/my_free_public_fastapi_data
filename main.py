from fastapi import FastAPI
from fastapi.responses import JSONResponse

from routes.user import router as user_router

from exceptions.user import UserNotFoundError, UserAlreadyExistsError


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

@app.exception_handler(UserAlreadyExistsError)
async def user_already_exists_handler(request, exc):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

app.include_router(user_router)