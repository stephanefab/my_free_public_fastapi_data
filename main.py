from fastapi import FastAPI, Path, HTTPException, Query
from schemas.product import ProductCreate, ProductUpdate, ProductPatch, ProductResponse
from schemas.user import UserCreate, UserUpdate, UserPatch, UserResponse, UserListResponse
from datas import products, next_product_id, users, next_user_id
from datetime import datetime
import math

app = FastAPI()

@app.post("/products", status_code=201, response_model=ProductResponse)
def create_product(product: ProductCreate):
    global next_product_id
    now = datetime.now()
    
    new_product = {
        "id": next_product_id,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity,
        "created_at": now,
        "updated_at": now
    }
    
    products.append(new_product)
    next_product_id += 1
    return new_product


def find_product(product_id: int):
    for p in products:
        if p['id'] == product_id:
            return p
    return None

@app.get("/products", response_model=list[ProductResponse])
def get_products():
    return products

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int = Path(ge=1)):
    product = find_product(product_id)
    
    if product is None:
        raise HTTPException(status_code=404, detail=f"le produit #{product_id} n'a pas été trouvé")
    
    return product

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_update: ProductUpdate, product_id: int = Path(ge=1)):
    product = find_product(product_id)
    
    if product is None:
        raise HTTPException(status_code=404, detail=f"le produit #{product_id} n'a pas été trouvé")
    
    product['name'] = product_update.name
    product['price'] = product_update.price
    product['quantity'] = product_update.quantity
    product['updated_at'] = datetime.now()
    
    return product

@app.patch("/products/{product_id}", response_model=ProductResponse)
def patch_product(product_patch: ProductPatch, product_id: int = Path(ge=1)):
    product = find_product(product_id)
    
    if product is None:
        raise HTTPException(status_code=404, detail=f"le produit #{product_id} n'a pas été trouvé")
    
    updates = product_patch.model_dump(exclude_none=True)
    for field, value in updates.items():
        product[field] = value

    product['updated_at'] = datetime.now()
    
    return product

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int = Path(ge=1)):
    product = find_product(product_id)
    
    if product is None:
            raise HTTPException(
                status_code=404,
                detail=f"Le produit #{product_id} n'a pas été trouvé"
            )
    
    products.remove(product)
    

def find_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    return None

def filter_users_by_role(users: list, role: str | None = None):
    if role is None:
        return users.copy()
    
    role = role.strip().lower()
    return [user for user in users if user["role"] == role]

def search_users(users: list, search: str | None = None):
    if search is None:
        return users.copy()
    
    search = search.strip().lower()
    return [user for user in users if (search in user["email"].lower() or search in user["username"].lower())]

def paginate_users(users: list, limit: int = 20, offset: int = 0):    
    end = offset + limit
    return users[offset:end]
    
@app.get("/users", response_model=UserListResponse)
def get_users(role: str | None = Query(default=None), search: str | None = Query(default=None), page: int = Query(default=1, ge=1), page_size: int = Query(default=20, ge=1, le=100)):
    filtered_users = filter_users_by_role(users, role)
    filtered_users = search_users(filtered_users, search)

    total = len(filtered_users)
    
    offset = (page - 1) * page_size
    items = paginate_users(filtered_users, page_size, offset)
    
    total_pages = math.ceil(total/page_size)
    
    has_next = page < total_pages
    has_previous = page > 1
    
    return {
        "items": items,
        "total": total,
        "total_pages": total_pages,
        "page": page,
        "page_size": page_size,
        "has_previous": has_previous,
        "has_next": has_next
    }

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int = Path(ge=1)):
    user = find_user(user_id)
    
    if user is None:
        raise HTTPException(status_code=404, detail=f"l'utilisateur #{user_id} n'a pas été trouvé")
    
    return user

@app.post(
    "/users",
    status_code=201,
    response_model=UserResponse
)
def create_user(user: UserCreate):
    global next_user_id

    now = datetime.now()

    new_user = {
        "id": next_user_id,
        "username": user.username,
        "email": user.email,
        "password_hash": "HASH À FAIRE PLUS TARD",
        "role": "user",
        "is_active": True,
        "created_at": now,
        "updated_at": now,
    }

    users.append(new_user)
    next_user_id += 1

    return new_user

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_update: UserUpdate,
    user_id: int = Path(ge=1)
):
    user = find_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"L'utilisateur #{user_id} n'a pas été trouvé"
        )

    user["username"] = user_update.username
    user["email"] = user_update.email
    user["password_hash"] = user_update.password + "HASHED PASSWORD"
    user["updated_at"] = datetime.now()

    return user


@app.patch("/users/{user_id}", response_model=UserResponse)
def patch_user(
    user_patch: UserPatch,
    user_id: int = Path(ge=1)
):
    user = find_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"L'utilisateur #{user_id} n'a pas été trouvé"
        )

    updates = user_patch.model_dump(exclude_unset=True)

    for field, value in updates.items():
        if field == "password":
            value = value + "HASHED PASSWORD"

        user[field] = value

    if updates:
        user["updated_at"] = datetime.now()

    return user

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int = Path(ge=1)):
    user = find_user(user_id)
    
    if user is None:
            raise HTTPException(
                status_code=404,
                detail=f"L'utilisateur #{user_id} n'a pas été trouvé"
            )
    
    users.remove(user)
