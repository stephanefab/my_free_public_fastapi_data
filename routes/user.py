from fastapi import APIRouter, HTTPException, Query, status

from schemas.user import (
    UserCreate,
    UserUpdate,
    UserPatch,
    UserResponse,
    UserListResponse,
)

from services import user as user_service


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "",
    response_model=UserListResponse
)
def get_users(
    role: str | None = Query(
        default=None
    ),

    search: str | None = Query(
        default=None
    ),

    page: int = Query(
        default=1,
        ge=1
    ),

    page_size: int = Query(
        default=20,
        ge=1,
        le=100
    ),
):
    return user_service.get_users(
        role=role,
        search=search,
        page=page,
        page_size=page_size
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(user_id: int):

    try:
        return user_service.get_user(user_id)

    except user_service.UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate):

    return user_service.create_user(user)


@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_id: int,
    user_update: UserUpdate
):

    try:
        return user_service.update_user(
            user_update,
            user_id
        )

    except user_service.UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )


@router.patch(
    "/{user_id}",
    response_model=UserResponse
)
def patch_user(
    user_id: int,
    user_patch: UserPatch
):

    try:
        return user_service.patch_user(
            user_patch,
            user_id
        )

    except user_service.UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(user_id: int):

    try:
        user_service.delete_user(user_id)

    except user_service.UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )