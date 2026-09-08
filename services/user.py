import math
from datetime import datetime

import datas
from schemas.user import UserCreate, UserUpdate, UserPatch

from exceptions.user import UserNotFoundError, UserAlreadyExistsError


def find_user(user_id: int):
    for user in datas.users:
        if user["id"] == user_id:
            return user

    return None


def email_already_exists(user_email: str):
    for user in datas.users:
        if user["email"] == user_email:
            return user

    return None

def get_user(user_id: int):
    user = find_user(user_id)

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
    if email_already_exists(user.email):
        raise UserAlreadyExistsError(
            "Cette adresse email existe déjà"
        )
        
    now = datetime.now()

    new_user = {
        "id": datas.next_user_id,
        "username": user.username,
        "email": user.email,

        # Temporaire pour notre exercice.
        # Plus tard : véritable password hashing.
        "password_hash": user.password + " HASHED",

        "role": "user",
        "is_active": True,
        "created_at": now,
        "updated_at": now,
    }

    datas.users.append(new_user)

    datas.next_user_id += 1

    return new_user


def update_user(
    user_update: UserUpdate,
    user_id: int
):
    user = find_user(user_id)

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
    user = find_user(user_id)

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
    user = find_user(user_id)

    if user is None:
        raise UserNotFoundError(
            f"L'utilisateur #{user_id} n'a pas été trouvé"
        )

    datas.users.remove(user)