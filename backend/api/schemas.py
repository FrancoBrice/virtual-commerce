from pydantic import BaseModel
from typing import List

class ProductRequest(BaseModel):
    productId: int
    price: float
    quantity: int

class CustomerData(BaseModel):
    name: str
    shipping_street: str
    commune: str
    phone: str

class CartRequest(BaseModel):
    products: List[ProductRequest]
    customer_data: CustomerData
