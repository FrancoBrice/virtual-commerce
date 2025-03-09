from services.cart_memory import cart_memory
from sqlalchemy.orm import Session
from models.models import Product

def store_cart(cart_data):
    cart_memory["cart"] = cart_data

def get_cart():
    print(cart_memory)
    return cart_memory.get("cart")

def validate_stock(cart_data, db: Session):
    for item in cart_data["products"]:
        product = db.query(Product).filter(Product.id == item["productId"]).first()
        if not product or item["quantity"] > product.stock_real:
            return False  

    return True  