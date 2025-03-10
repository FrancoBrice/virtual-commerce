from fastapi import APIRouter, HTTPException, Depends, status
import requests
import random
from sqlalchemy.orm import Session
from utils.helpers import print_cart_summary
from services.cart_service import store_cart, validate_cart_stock, get_cart_items
from services.shipping_service import calculate_best_shipping_option
from api.dependencies import get_db
from api.schemas import CartRequest
from models.database import SessionLocal
from models.models import Cart, CartProductAssociation, Product

router = APIRouter()

@router.post("/api/cart", response_model=dict)
def create_cart(cart_request: CartRequest, db: Session = Depends(get_db)):
    validate_cart_stock(cart_request, db)

    cart_items = get_cart_items(cart_request, db)

    best_option = calculate_best_shipping_option(cart_items, cart_request.customer_data, db)

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
    
    try:
        new_cart_id = store_cart(cart_data) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    with SessionLocal() as session:
        stored_cart = session.query(Cart).filter_by(id=new_cart_id).first()
        if not stored_cart:
            raise HTTPException(status_code=500, detail="Error retrieving the stored cart.")

        formatted_cart = {
            "id": stored_cart.id,
            "total": stored_cart.total,  
            "discountedTotal": stored_cart.discounted_total,  
            "products": [
                {
                    "id": item.product.id,
                    "name": item.product.title,
                    "price": item.product.price,
                    "discountPercentage": item.product.discount_percentage,
                    "quantity": item.quantity,
                    "stock_obtained": item.product.stock,
                    "rating": item.product.rating,
                    "stock_real": item.product.stock_real,
                    "thumbnail": item.product.thumbnail  
                }
                for item in stored_cart.products
            ]
        }
    print("en api", cart_data)
    print_cart_summary(cart_data)
    return formatted_cart
  
  
@router.delete("/api/cart/{cart_id}", response_model=dict)
def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()

    if not cart:
        raise HTTPException(status_code=404, detail=f"Cart with ID {cart_id} not found.")

    db.query(CartProductAssociation).filter(CartProductAssociation.cart_id == cart_id).delete()

    db.delete(cart)
    db.commit()

    return {"message": f"Cart {cart_id} deleted successfully."}


@router.post("/api/validate-stock", status_code=status.HTTP_200_OK)
def validate_stock(cart_id: int, db: Session = Depends(get_db)):
    """Valida que el stock real de los productos del carrito sea suficiente."""
    
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=400, detail="Cart not found.")

    cart_items = (
        db.query(CartProductAssociation, Product)
        .join(Product, CartProductAssociation.product_id == Product.id)
        .filter(CartProductAssociation.cart_id == cart.id)
        .all()
    )

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty.")

    for cart_product, product in cart_items:
        if cart_product.quantity > product.stock_real:
            raise HTTPException(
                status_code=400, 
                detail=f"Stock cannot be fulfilled for product {product.title}. Requested: {cart_product.quantity}, Available: {product.stock_real}"
            )

    return {"message": "Stock validated successfully."}