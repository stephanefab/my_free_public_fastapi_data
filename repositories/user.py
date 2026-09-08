import datas
from schemas.user import UserCreate
from datetime import datetime

def find_by_id(user_id: int):
    for user in datas.users:
        if user["id"] == user_id:
            return user
    return None

def find_by_email(user_email: str):
    normalized_email = user_email.strip().lower()
    
    for user in datas.users:
        if user["email"].strip().lower() == normalized_email:
            return user
    return None

def find_by_username(user_username: str):
    normalized_username = user_username.strip().lower()
    
    for user in datas.users:
        if user["username"].strip().lower() == normalized_username:
            return user
    return None

def create(email: str, username: str, password_hash: str, role: str, is_active: bool):
    now = datetime.now()

    new_user = {
        "id": datas.next_user_id,
        "username": username,
        "email": email,
        "password_hash": password_hash,
        "role": "user",
        "is_active": True,
        "created_at": now,
        "updated_at": now,
    }

    datas.users.append(new_user)
    datas.next_user_id += 1
    
    return new_user