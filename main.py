from fastapi import FastAPI, Header, Path, Query
from pydantic import BaseModel

app = FastAPI()

class OrderCreate(BaseModel):
    product_id: int
    quantity: int


@app.post("/orders/{order_id}")
def create_order(order: OrderCreate, order_id: int = Path(ge=1), priority: int = Query(default=1, ge=1, le=5), x_client_name: str | None = Header(default=None)):
    return {
        "order_id": order_id,
        "priority": priority,
        "client": x_client_name,
        "product_id": order.product_id,
        "quantity": order.quantity
    }