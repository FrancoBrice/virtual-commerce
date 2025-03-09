from fastapi import APIRouter, HTTPException
import os
from services.shipping_service import get_best_shipping_rate

router = APIRouter()

@router.post("/api/get-lowest-shipping-rate")
def get_lowest_shipping_rate():
    best_option = get_best_shipping_rate()
    if not best_option:
        raise HTTPException(status_code=400, detail="No available shipping rates.")
    return best_option
