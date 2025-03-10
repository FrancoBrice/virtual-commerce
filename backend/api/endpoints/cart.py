from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from services.cart_service import store_cart, validate_cart_stock, get_cart_items, fetch_random_cart, format_stored_cart
from services.shipping_service import calculate_best_shipping_option
from services.update_db import update_products
from api.dependencies import get_db
from api.schemas import CartRequest
from models.database import SessionLocal
from models.models import Cart, CartProductAssociation, Product
from utils.helpers import print_cart

router = APIRouter()


@router.post("/api/cart", response_model=dict)
async def create_cart(cart_request: CartRequest, db: Session = Depends(get_db)):

    await update_products()
    
    cart_items = get_cart_items(cart_request, db)
    print_cart(cart_items, db)

    validate_cart_stock(cart_request, db)

    best_option = calculate_best_shipping_option(cart_items, cart_request.customer_data, db)
    if not best_option:
        raise HTTPException(status_code=400, detail="No available shipping rates.")

    return best_option
  
@router.post("/api/cart/random")
async def generate_cart():
    await update_products()  

    cart_data = fetch_random_cart()

    try:
        new_cart_id = store_cart(cart_data)  
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return format_stored_cart(new_cart_id)

@router.delete("/api/cart/{cart_id}", response_model=dict)
def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()

    if not cart:
        raise HTTPException(status_code=404, detail=f"Cart with ID {cart_id} not found.")

    db.query(CartProductAssociation).filter(CartProductAssociation.cart_id == cart_id).delete()
    db.delete(cart)
    db.commit()
    return {"message": f"Cart {cart_id} deleted successfully."}

