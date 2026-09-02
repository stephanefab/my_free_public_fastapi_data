from fastapi import FastAPI, Path, HTTPException, Header, Query
from pydantic import BaseModel, field_validator, model_validator, Field

app = FastAPI()


products = [
    {"id": 1, "name": "Clavier", "price": 2500, "quantity": 9, "internal_cost": 700},
    {"id": 2, "name": "Souris", "price": 1500, "quantity": 11},
    {"id": 3, "name": "Ecran", "price": 25000, "quantity": 16},
]
next_product_id = 4


class ProductCreate(BaseModel):
    name: str = Field(min_length=2)
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()

        if not value:
            raise ValueError(
                "Le nom ne peut pas contenir uniquement des espaces"
            )

        return value.lower()

    @model_validator(mode="after")
    def validate_product(self):
        if self.price == 0 and self.quantity == 0:
            raise ValueError(
                "Un produit gratuit doit avoir une quantité supérieure à 0"
            )
        
        return self
    
class ProductUpdate(BaseModel):
    name: str
    price: float
    quantity: int

class ProductPatch(BaseModel):
    name: str | None = None
    price: float | None = None
    quantity: int | None = None

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    quantity: int

def find_product(product_id: int):
    for product in products:
        if product['id'] == product_id:
            return product
    return None


@app.get("/products")
def get_products():
    return products


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int = Path(ge=1)):
    product = find_product(product_id)
    
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Produit introuvable"
        )
    
    return product


@app.post("/products", status_code=201)
def create_product(product: ProductCreate):
    global next_product_id
    
    new_id = next_product_id
    next_product_id += 1
    
    new_product = {
        "id": new_id,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity,
    }
    
    products.append(new_product)
    return new_product


@app.put("/products/{product_id}", status_code=200)
def update_product(product_update: ProductUpdate, product_id: int = Path(ge=1)):
    product = find_product(product_id)
        
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Produit introuvable"
        )
    
    product['name'] = product_update.name
    product['price'] = product_update.price
    product['quantity'] = product_update.quantity
    
    return product


@app.patch("/products/{product_id}", status_code=200)
def patch_product(product_patch: ProductPatch, product_id: int = Path(ge=1)):
    product = find_product(product_id)
        
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Produit introuvable"
        )
    
    updates = product_patch.model_dump(exclude_unset=True)
    
    for field, value in updates.items():
        product[field] = value
    
    return product


@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int = Path(ge=1)):
    product = find_product(product_id)
    
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Produit introuvable"
        )
    
    products.remove(product)
