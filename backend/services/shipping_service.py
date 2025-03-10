import os
import requests
from sqlalchemy.orm import Session
from models.models import Product
from fastapi import HTTPException
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


SENDER_INFO = {
    "type": "PICK_UP",
    "addressStreet": "Juan de Valiente 3630",
    "city": "Vitacura",
    "phone": "+56912345678",
    "name": "Flapp Store"
}

TRAELOYA_API_URL = os.getenv("TRAELOYA_API_URL")
UDER_API_URL = os.getenv("UDER_API_URL")
UDER_API_KEY = os.getenv("UDER_API_KEY")
TRAELOYA_API_KEY = os.getenv("TRAELOYA_API_KEY")

def calculate_best_shipping_option(cart_items, customer_data, db):
    shipping_request = {
        "products": cart_items,
        "customer_data": customer_data
    }
    best_option = get_best_shipping_rate(db, shipping_request) 
    print("🚚 Best courier option:", best_option)
    return best_option
  
def get_best_shipping_rate(db: Session, cart_data: dict):
    if not cart_data:
        raise HTTPException(status_code=400, detail="Cart data is missing.")

    receiver_info = format_receiver_info(cart_data["customer_data"])
    waypoints = [SENDER_INFO, receiver_info]
    items = extract_items_from_cart(cart_data, db)

    traeloya_price = get_traeloya_rate(waypoints, items)
    uder_price = get_uder_rate(waypoints, items)

    shipping_options = []
    if traeloya_price is not None:
        shipping_options.append({"courier": "TraeloYa", "price": traeloya_price})
    if uder_price is not None:
        shipping_options.append({"courier": "Uder", "price": uder_price})

    if not shipping_options:
        raise HTTPException(status_code=400, detail="No available shipping rates from any courier.")

    return min(shipping_options, key=lambda x: x["price"])


def format_receiver_info(customer_data):
    return {
        "type": "DROP_OFF",
        "addressStreet": customer_data.shipping_street,
        "city": customer_data.commune,
        "phone": customer_data.phone,
        "name": customer_data.name
    }


def extract_items_from_cart(cart_data, db: Session):
    product_ids = [item["id"] for item in cart_data["products"]]

    products_in_db = db.query(Product).filter(Product.id.in_(product_ids)).all()
    product_dict = {p.id: p for p in products_in_db}

    extracted_items = []
    for item in cart_data["products"]:
        product_info = product_dict.get(item["id"])
        if not product_info:
            continue  

        if not all([product_info.width, product_info.height, product_info.depth, product_info.weight]):
            raise HTTPException(status_code=400, detail=f"Product {product_info.title} is missing required dimensions or weight.")

        volume = product_info.width * product_info.height * product_info.depth * item["quantity"]

        extracted_items.append({
            "id": product_info.id,
            "name": product_info.title,
            "quantity": item["quantity"],
            "value": product_info.price,
            "price": product_info.price,
            "weight": product_info.weight,
            "volume": volume,
            "dimensions": {
                "width": product_info.width,
                "height": product_info.height,
                "depth": product_info.depth
            }
        })

    return extracted_items


def get_traeloya_rate(waypoints, items):
    headers = {
        "X-Api-Key": TRAELOYA_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "items": items,
        "waypoints": waypoints
    }

    try:
        response = requests.post(TRAELOYA_API_URL, json=payload, headers=headers, verify=False)
        response.raise_for_status()
        rates = response.json()

        if "deliveryOffers" in rates and "pricing" in rates["deliveryOffers"]:
            return rates["deliveryOffers"]["pricing"]["total"]

    except requests.RequestException as e:
        print(f"Error al obtener tarifa de TraeloYa: {e}")
    return None


def get_uder_rate(waypoints, items):
    headers = {
        "X-Api-Key": UDER_API_KEY,
        "Content-Type": "application/json"
    }
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
                "weight": item["weight"],
                "dimensions": item["dimensions"]
            }
            for item in items
        ]
    }

    try:
        response = requests.post(UDER_API_URL, json=payload, headers=headers, verify=False)
        response.raise_for_status()
        rates = response.json()

        if "fee" in rates:
            return rates["fee"]
        elif "error" in rates:
            print(f"Uder API error: {rates['error']}")

    except requests.RequestException as e:
        print(f"Error al obtener tarifa de Uder: {e}")
    return None
