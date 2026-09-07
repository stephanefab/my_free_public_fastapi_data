from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, model_validator


class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50
    )

    email: EmailStr

    password: str = Field(
        min_length=8
    )


class UserUpdate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50
    )

    email: EmailStr

    password: str = Field(
        min_length=8
    )


class UserPatch(BaseModel):
    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=50
    )

    email: EmailStr | None = None

    password: str | None = Field(
        default=None,
        min_length=8
    )

    @model_validator(mode="after")
    def validate_patch(self):
        if "password" in self.model_fields_set and self.password is None:
            raise ValueError(
                "Le mot de passe ne peut pas être null"
            )

        return self


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserListResponse(BaseModel):
    items: list[UserResponse]

    total: int
    total_pages: int

    page: int
    page_size: int

    has_previous: bool
    has_next: bool