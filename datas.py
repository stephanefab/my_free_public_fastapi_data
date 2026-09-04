from datetime import datetime

products = [
    {
        "id": 1,
        "name": "Clavier",
        "price": 2500,
        "quantity": 10,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    },
    {
        "id": 2,
        "name": "Souris",
        "price": 1500,
        "quantity": 20,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    },
]

next_product_id = 3

users = [
    {
        "id": 1,
        "username": "username",
        "email": "email@example.com",
        "password_hash": "HASH À FAIRE PLUS TARD",
        "role": "user",
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
]
next_user_id = 2