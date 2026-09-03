from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

class Address(BaseModel):
    street: str = Field(min_length=2)
    city: str = Field(min_length=2)
    country: str = Field(min_length=2)
    
    @field_validator("street", mode="before")
    @classmethod
    def validate_street(cls, value):
        value = value.strip().lower()
        
        if not value:
            raise ValueError("'street' ne peux pas être vide")
        return value
    
    @field_validator("city", mode="before")
    @classmethod
    def validate_city(cls, value):
        value = value.strip().lower()
        
        if not value:
            raise ValueError("'city' ne peux pas être vide")
        return value
    
    @field_validator("country", mode="before")
    @classmethod
    def validate_country(cls, value):
        value = value.strip().lower()
        
        if not value:
            raise ValueError("'country' ne peux pas être vide")
        return value

class UserCreate(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(ge=18)
    email: EmailStr
    address: Address
    
    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value):
        value = value.strip().lower()
        
        if not value:
            raise ValueError("'name' ne peux pas être vide")
        return value


class OrderItem(BaseModel):
    product_id: int = Field(ge=1)
    quantity: int = Field(ge=1)
    unit_price: float = Field(ge=0)
    
    @model_validator(mode="after")
    def validate_item(self):
        if self.quantity >= 10 and self.unit_price > 1000:
            raise ValueError(
                "Pour une quantité >= 10, le prix unitaire doit être <= 1000"
            )

        return self
    
class OrderCreate(BaseModel):
    customer_name: str = Field(min_length=2)
    items: list[OrderItem] = Field(min_length=1, max_length=50) # forcer l'existence d'au moins un élément