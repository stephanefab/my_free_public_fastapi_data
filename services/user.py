import math
from datetime import datetime

import datas
from schemas.user import UserCreate, UserUpdate, UserPatch

from exceptions.user import UserNotFoundError, UserAlreadyExistsError

from repositories import user as user_repository


def find_user_by_email(user_email: str):
    normalized_email = user_email.strip().lower()
    for user in datas.users:
        if user["email"].strip().lower() == normalized_email:
            return user

    return None


def find_user_by_username(user_username: str):
    normalized_username = user_username.strip().lower()
    for user in datas.users:
        if user["username"].strip().lower() == normalized_username:
            return user

    return None


def get_user(user_id: int):
    user = user_repository.find_by_id(user_id)

    if user is None:
        raise UserNotFoundError(
            f"L'utilisateur #{user_id} n'a pas été trouvé"
        )

    return user


def filter_users_by_role(
    users: list,
    role: str | None = None
):
    if role is None:
        return users.copy()

    role = role.strip().lower()

    return [
        user
        for user in users
        if user["role"].lower() == role
    ]


def search_users(
    users: list,
    search: str | None = None
):
    if search is None:
        return users.copy()

    search = search.strip().lower()

    if search == "":
        return users.copy()

    return [
        user
        for user in users
        if (
            search in user["email"].lower()
            or search in user["username"].lower()
        )
    ]


def paginate_users(
    users: list,
    page: int = 1,
    page_size: int = 20
):
    if page < 1:
        raise ValueError(
            "'page' doit être supérieur ou égal à 1"
        )

    if page_size < 1 or page_size > 100:
        raise ValueError(
            "'page_size' doit être compris entre 1 et 100 inclus"
        )

    offset = (page - 1) * page_size
    end = offset + page_size

    return users[offset:end]


def get_users(
    role: str | None = None,
    search: str | None = None,
    page: int = 1,
    page_size: int = 20
):
    filtered_users = filter_users_by_role(
        datas.users,
        role
    )

    filtered_users = search_users(
        filtered_users,
        search
    )

    total = len(filtered_users)

    items = paginate_users(
        filtered_users,
        page,
        page_size
    )

    total_pages = max(
        1,
        math.ceil(total / page_size)
    )

    has_previous = page > 1
    has_next = page < total_pages

    return {
        "items": items,
        "total": total,
        "total_pages": total_pages,
        "page": page,
        "page_size": page_size,
        "has_previous": has_previous,
        "has_next": has_next,
    }


def create_user(user: UserCreate):
    existing_user = user_repository.find_by_email(user.email)
    if existing_user is not None:
        raise UserAlreadyExistsError(
            "Cette adresse email existe déjà",
            "USER_EMAIL_EXISTS"
        )
    
    existing_user = user_repository.find_by_username(user.username)
    if existing_user is not None:
        raise UserAlreadyExistsError(
            "Cet username existe déjà",
            "USER_USERNAME_EXISTS"
        )
    
    hashed_password = user.password + "@@#HASHED@@#__h45h3d"
    new_user = user_repository.create(email=user.email, username=user.username, password_hash=hashed_password, role="user", is_active=False) 
    return new_user


def update_user(
    user_update: UserUpdate,
    user_id: int
):
    user = user_repository.find_by_id(user_id)

    if user is None:
        raise UserNotFoundError(
            f"L'utilisateur #{user_id} n'a pas été trouvé"
        )

    user["username"] = user_update.username
    user["email"] = user_update.email

    # Temporaire pour notre exercice.
    user["password_hash"] = (
        user_update.password + " HASHED"
    )

    user["updated_at"] = datetime.now()

    return user


def patch_user(
    user_patch: UserPatch,
    user_id: int
):
    user = user_repository.find_by_id(user_id)

    if user is None:
        raise UserNotFoundError(
            f"L'utilisateur #{user_id} n'a pas été trouvé"
        )

    updates = user_patch.model_dump(
        exclude_unset=True
    )

    for field, value in updates.items():

        if field == "password":
            value = value + " HASHED"

            user["password_hash"] = value

        else:
            user[field] = value

    if updates:
        user["updated_at"] = datetime.now()

    return user


def delete_user(user_id: int):
    user = user_repository.find_by_id(user_id)

    if user is None:
        raise UserNotFoundError(
            f"L'utilisateur #{user_id} n'a pas été trouvé"
        )

    datas.users.remove(user)