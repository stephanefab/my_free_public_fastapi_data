from fastapi import FastAPI
from models import UserCreate, OrderCreate

app = FastAPI()

@app.post("/api/users")
def create_user(user: UserCreate):
    return user

@app.post("/api/orders")
def create_order(order: OrderCreate):
    return order