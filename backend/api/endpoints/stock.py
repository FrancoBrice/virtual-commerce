from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.models import Product
from api.dependencies import get_db
from services.cart_service import get_cart  # Se mantiene igual

router = APIRouter()

@router.post("/api/validate-stock", status_code=status.HTTP_200_OK)
def validate_stock(db: Session = Depends(get_db)):
    cart_data = get_cart()
    if not cart_data:
        raise HTTPException(status_code=400, detail="No cart available.")

    for item in cart_data["products"]:
        product = db.query(Product).filter(Product.id == item["productId"]).first()
        if not product or item["quantity"] > product.stock_real:
            raise HTTPException(status_code=400, detail="Stock cannot be fulfilled.")

    return {"message": "Stock validated successfully."}
