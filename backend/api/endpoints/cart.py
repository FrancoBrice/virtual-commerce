from fastapi import APIRouter, HTTPException
import requests
import random
from utils.helpers import print_cart
from services.cart_service import store_cart

router = APIRouter()

cart_memory = {}

@router.post("/api/generate-cart")
def generate_cart():
    random_id = random.randint(1, 50)
    response = requests.get(f"https://dummyjson.com/carts/{random_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="No cart available.")

    cart_data = response.json()
    store_cart(cart_data)
    print_cart(cart_data)
    return cart_data
