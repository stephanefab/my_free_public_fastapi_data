from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


ProductName = Annotated[
    str,
    Field(min_length=2, max_length=100)
]

ProductPrice = Annotated[
    float,
    Field(ge=0)
]

ProductQuantity = Annotated[
    int,
    Field(ge=0)
]


class ProductCreate(BaseModel):
    name: ProductName
    price: ProductPrice
    quantity: ProductQuantity


class ProductUpdate(BaseModel):
    name: ProductName
    price: ProductPrice
    quantity: ProductQuantity


class ProductPatch(BaseModel):
    name: ProductName | None = None
    price: ProductPrice | None = None
    quantity: ProductQuantity | None = None


class ProductResponse(BaseModel):
    id: int
    name: ProductName
    price: ProductPrice
    quantity: ProductQuantity
    created_at: datetime
    updated_at: datetime