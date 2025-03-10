from fastapi import HTTPException
from api.schemas import CartRequest
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.models import Cart, Product, CartProductAssociation

def store_cart(cart_data: dict):
    with SessionLocal() as session:
        new_cart = Cart(
            total=cart_data["total"],
            discounted_total=cart_data["discountedTotal"]
        )
        session.add(new_cart)
        session.commit()  

        for item in cart_data["products"]:
            product = session.query(Product).filter_by(id=item["id"]).first()
            cart_product = CartProductAssociation(
                cart_id=new_cart.id,
                product_id=product.id,
                quantity=item["quantity"]
            )
            session.add(cart_product)

        session.commit()

        return new_cart.id  

def validate_cart_stock(cart_request: CartRequest, db: Session):
    for item in cart_request.products:
        product = db.query(Product).filter(Product.id == item.productId).first()

        if not product:
            raise HTTPException(status_code=404, detail=f"Product ID {item.productId} not found.")

        if item.quantity > product.stock_real:
            raise HTTPException(
                status_code=400,
                detail=f"Stock cannot be fulfilled for {product.title}. Requested: {item.quantity}, Available: {product.stock_real}"
            )

def get_cart_items(cart_request: CartRequest, db: Session):
    product_ids = [item.productId for item in cart_request.products]
    products_in_db = db.query(Product).filter(Product.id.in_(product_ids)).all()
    product_dict = {p.id: p for p in products_in_db}

    cart_items = []
    for item in cart_request.products:
        product_info = product_dict.get(item.productId)
        if not product_info:
            continue

        cart_items.append({
            "id": product_info.id,  
            "name": product_info.title,
            "quantity": item.quantity,
            "value": product_info.price,  
            "price": product_info.price,  
            "weight": product_info.weight,
            "dimensions": {
                "width": product_info.width,
                "height": product_info.height,
                "depth": product_info.depth
            }
        })

    return cart_items