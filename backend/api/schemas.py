from pydantic import BaseModel
from typing import List

class ProductItem(BaseModel):
    productId: str
    price: float
    quantity: int
    discount: float

class CustomerData(BaseModel):
    name: str
    shipping_street: str
    commune: str
    phone: str

class CartRequest(BaseModel):
    products: List[ProductItem]
    customer_data: CustomerData

class CartResponse(BaseModel):
    courier: str
    price: float

class ErrorResponse(BaseModel):
    error: str
