from models.database import SessionLocal
from sqlalchemy.orm import Session
from models.models import Product, Cart, CartProductAssociation

def get_db():
    db = SessionLocal()
    try:
        yield db  
    finally:
        db.close() 
        
        
def print_cart(cart_items, db):
    print("\n📦 **Carrito generado:**")
    with SessionLocal() as session:
        for item in cart_items:
            product = session.query(Product).filter_by(id=item["id"]).first()
            if product:
                class CartItem:
                    def __init__(self, data):
                        self.id = data["id"]
                        self.quantity = data["quantity"]

                cart_item = CartItem(item)

                print_product(cart_item, product)

def print_product(item, product):
  print(f"🔢 ID: {product.id}")
  print(f"📌 Nombre: {product.title}")
  print(f"💲 Precio por unidad: ${product.price:.2f}")
  print(f"💰 Descuento total: {product.discount_percentage:.2f}%")
  print(f"📦 Cantidad solicitada: {item.quantity}")
  print(f"🏪 Stock obtenido: {product.stock}")
  print(f"⭐ Rating: {product.rating}")
  print(f"📊 Stock real: {product.stock_real}\n")