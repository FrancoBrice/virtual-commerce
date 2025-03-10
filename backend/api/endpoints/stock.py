from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from services.cart_service import validate_cart_stock
from api.dependencies import get_db
from api.schemas import CartRequest

router = APIRouter()

@router.post("/api/validate-stock", status_code=status.HTTP_200_OK)
def validate_stock(cart_request: CartRequest, db: Session = Depends(get_db)):
    validate_cart_stock(cart_request, db)  
    return {"message": "Stock validated successfully."}