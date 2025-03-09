from fastapi import APIRouter, HTTPException, status, Depends
from . import schemas
from services import cart_service
import random
import requests
import json
import utils.helpers as helpers
from models.database import SessionLocal
from models.models import Product
from utils.helpers import get_db
from sqlalchemy.orm import Session  
import os


router = APIRouter()

cart_memory = {}

@router.post("/api/cart", response_model=schemas.CartResponse)
async def create_cart(cart_request: schemas.CartRequest):
    """
    Endpoint to process the cart and obtain the best shipping rate.
    """
    try:
        quote = await cart_service.process_cart(cart_request)
        return quote
    except ValueError as ve:
        # Return a 400 error if there is a validation or business logic issue
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        # In case of unexpected errors, return a 500 error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.post("/api/generate-cart", response_model=dict)
def generate_cart():
    try:
        random_id = random.randint(1, 50)
        response = requests.get(f"https://dummyjson.com/carts/{random_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se pudo obtener el carrito")
        
        cart_data = response.json()
        cart_memory["cart"] = cart_data  
        helpers.print_cart(cart_data)
        
        return cart_data

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    
@router.post("/api/validate-stock", status_code=status.HTTP_200_OK)
def validate_stock(db: Session = Depends(get_db)):
    if "cart" not in cart_memory or not cart_memory["cart"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No cart available.")

    cart_data = cart_memory["cart"]

    for item in cart_data["products"]:
        product = db.query(Product).filter(Product.id == item["id"]).first()

        if not product or item["quantity"] > product.stock_real:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Stock cannot be fulfilled.")

    return {"message": "Stock validated successfully."}  


@router.post("/api/get-lowest-shipping-rate", response_model=dict)
def get_lowest_shipping_rate():
    if "cart" not in cart_memory or not cart_memory["cart"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No cart available.")

    cart_data = cart_memory["cart"]

    sender_info = {
        "type": "PICK_UP",
        "addressStreet": "Juan de Valiente 3630",
        "city": "Vitacura",
        "phone": "+56912345678",
        "name": "Flapp Store"
    }

    receiver_info = {
        "type": "DROP_OFF",
        "addressStreet": "Avenida1212121",
        "city": "hola",
        "phone": "+56987654321",
        "name": "Juan Pérez"
    }

    waypoints = [sender_info, receiver_info]
    items = extract_items_from_cart(cart_data)

    traloya_price = get_courier_rate(
        "TraeloYa",
        os.getenv("TRALEOYA_API_URL"),
        os.getenv("TRALEOYA_API_KEY"),
        waypoints,
        items
    )

    uder_price = get_courier_rate(
        "Uder",
        os.getenv("UDER_API_URL"),
        os.getenv("UDER_API_KEY"),
        waypoints,
        items
    )

    if traloya_price is None and uder_price is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No available shipping rates.")

    shipping_options = []
    if traloya_price is not None:
        shipping_options.append({"courier": "TraeloYa", "price": traloya_price})
    if uder_price is not None:
        shipping_options.append({"courier": "Uder", "price": uder_price})

    best_option = min(shipping_options, key=lambda x: x["price"])


    print(f"Best shipping option: {best_option}")

    return best_option



def extract_items_from_cart(cart_data):
    return [
        {
            "name": item["title"],  # Required for Uder API
            "quantity": item["quantity"],
            "value": item["price"],
            "volume": 1.0  # Placeholder, TraeloYa format
        }
        for item in cart_data["products"]
    ]



def get_courier_rate(courier_name, api_url, api_key, waypoints, items):
    if not api_url or not api_key:
        return None

    headers = {
        "X-Api-Key": api_key,
        "Content-Type": "application/json"
    }

    if courier_name == "TraeloYa":
        payload = {
            "items": items,
            "waypoints": waypoints
        }
    elif courier_name == "Uder":
        payload = {
            "pickup_address": waypoints[0]["addressStreet"],
            "pickup_name": waypoints[0]["name"],
            "pickup_phone_number": waypoints[0]["phone"],
            "dropoff_address": waypoints[1]["addressStreet"],
            "dropoff_name": waypoints[1]["name"],
            "dropoff_phone_number": waypoints[1]["phone"],
            "manifest_items": [
                {
                    "name": item["name"],
                    "quantity": item["quantity"],
                    "price": item["value"],
                    "dimensions": {
                        "length": 10,  # Placeholder, replace with real dimensions if available
                        "height": 5,
                        "depth": 3
                    }
                }
                for item in items
            ]
        }
    else:
        return None

    print(f"Sending request to {courier_name}: {api_url}")
    print(f"Headers: {headers}")
    print(f"Payload: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(api_url, json=payload, headers=headers, verify=False)
        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.text}")

        response.raise_for_status()
        rates = response.json()

        if courier_name == "TraeloYa":
            return rates["deliveryOffers"]["pricing"]["total"]


        elif courier_name == "Uder":
            return rates["fee"]


    except Exception as e:
        print(f"Error fetching rate from {courier_name}: {e}")
        return None
