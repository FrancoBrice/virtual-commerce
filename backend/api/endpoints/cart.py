from fastapi import APIRouter, HTTPException, Depends
import requests
import random
from sqlalchemy.orm import Session
from utils.helpers import print_cart
from services.cart_service import store_cart, get_cart, validate_stock
from services.shipping_service import get_best_shipping_rate  
from api.dependencies import get_db
from api.schemas import CartRequest

router = APIRouter()

@router.post("/api/cart", response_model=dict)
def create_cart(cart_request: CartRequest, db: Session = Depends(get_db)):
    cart_data = cart_request.dict()

    if not validate_stock(cart_data, db):
        raise HTTPException(status_code=400, detail="Stock cannot be fulfilled.")
    store_cart(cart_data) 

    best_option = get_best_shipping_rate(db)
    if not best_option:
        raise HTTPException(status_code=400, detail="No available shipping rates.")

    return best_option
  

@router.post("/api/generate-random-cart")
def generate_cart():
    random_id = random.randint(1, 50)
    response = requests.get(f"https://dummyjson.com/carts/{random_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="No cart available.")

    cart_data = response.json()
    store_cart(cart_data)  
    return cart_data
