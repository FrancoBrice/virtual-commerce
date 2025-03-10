import json 
from models.database import SessionLocal
from sqlalchemy.orm import Session
from models.models import Product, Cart, CartProductAssociation

def print_cart(cart_data: dict, db: Session):
    cart_id = cart_data["id"]
    products_in_cart = cart_data["products"]
    
    print(f"🛒 Cart ID: {cart_id}")

    for item in products_in_cart:
        product_id = item["id"]
        
        # 🔍 Buscar producto en la BDD
        product = db.query(Product).filter(Product.id == product_id).first()

        if not product:
            print(f"⚠️ Warning: Product ID {product_id} not found in DB")
            continue  # Saltar este producto si no existe en la BDD
        
        # 🔄 Completar datos faltantes
        item["description"] = product.description
        item["stock"] = product.stock
        item["rating"] = product.rating
        item["stock_real"] = product.stock_real  # Usar propiedad calculada
        item["weight"] = product.weight
        item["dimensions"] = {
            "width": product.width,
            "height": product.height,
            "depth": product.depth
        }

        # 📌 Imprimir datos completos
        print(f"📦 Product ID: {product_id}")
        print(f"   🔹 Title: {item['title']}")
        print(f"   📖 Description: {item['description']}")
        print(f"   💰 Price per unit: ${item['price']}")
        print(f"   📉 Discount: {item['discountPercentage']}%")
        print(f"   🛍️ Quantity: {item['quantity']}")
        print(f"   🏬 Stock: {item['stock']}")
        print(f"   ⭐ Rating: {item['rating']}")
        print(f"   🔢 Real Stock: {item['stock_real']}")
        print(f"   📏 Dimensions: {item['dimensions']}")
        print(f"   ⚖️ Weight: {item['weight']}")
        print(f"   🖼️ Thumbnail: {item['thumbnail']}")
        print("-" * 40)

    # 🧾 Imprimir total del carrito
    print(f"💵 Total: ${cart_data['total']}")
    print(f"🎯 Discounted Total: ${cart_data['discountedTotal']}")


def get_db():
    db = SessionLocal()
    try:
        yield db  # Proporciona la sesión a la ruta
    finally:
        db.close() 