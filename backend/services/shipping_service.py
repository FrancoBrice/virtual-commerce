import os
import requests
import json
from sqlalchemy.orm import Session
from services.cart_service import get_cart
from models.models import Product  # ✅ Importar modelo de productos
from api.dependencies import get_db  # ✅ Obtener sesión de la base de datos

SENDER_INFO = {
    "type": "PICK_UP",
    "addressStreet": "Juan de Valiente 3630",
    "city": "Vitacura",
    "phone": "+56912345678",
    "name": "Flapp Store"
}

TRALEOYA_API_URL = os.getenv("TRALEOYA_API_URL")
UDER_API_URL = os.getenv("UDER_API_URL")
UDER_API_KEY = os.getenv("UDER_API_KEY")
TRALEOYA_API_KEY = os.getenv("TRALEOYA_API_KEY")


def get_best_shipping_rate(db: Session):
    cart_data = get_cart()
    if not cart_data:
        return None

    receiver_info = format_receiver_info(cart_data["customer_data"])
    waypoints = [SENDER_INFO, receiver_info]
    items = extract_items_from_cart(cart_data, db)  # ✅ Pasar sesión de BDD

    traloya_price = get_courier_rate("TraeloYa", TRALEOYA_API_URL, TRALEOYA_API_KEY, waypoints, items)
    uder_price = get_courier_rate("Uder", UDER_API_URL, UDER_API_KEY, waypoints, items)

    shipping_options = []
    if traloya_price:
        shipping_options.append({"courier": "TraeloYa", "price": traloya_price})
    if uder_price:
        shipping_options.append({"courier": "Uder", "price": uder_price})

    return min(shipping_options, key=lambda x: x["price"]) if shipping_options else None


def format_receiver_info(customer_data):
    return {
        "type": "DROP_OFF",
        "addressStreet": customer_data["shipping_street"],
        "city": customer_data["commune"],
        "phone": customer_data["phone"],
        "name": customer_data["name"]
    }


def extract_items_from_cart(cart_data, db: Session):
    extracted_items = []

    for item in cart_data["products"]:
        product_info = get_product_from_db(item["productId"], db)  # ✅ Obtener datos desde la BDD
        if not product_info:
            continue  

        extracted_items.append({
            "name": product_info.title,  # ✅ Nombre obtenido de la BDD
            "quantity": item["quantity"],
            "value": item["price"],
            "volume": 1.0  
        })

    return extracted_items


def get_product_from_db(product_id, db: Session):
    return db.query(Product).filter(Product.id == product_id).first()


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
                        "length": 10,
                        "height": 5,
                        "depth": 3
                    }
                }
                for item in items
            ]
        }
    else:
        return None

    try:
        response = requests.post(api_url, json=payload, headers=headers, verify=False)
        response.raise_for_status()
        rates = response.json()

        if courier_name == "TraeloYa":
            return rates["deliveryOffers"]["pricing"]["total"]
        elif courier_name == "Uder":
            return rates["fee"]

    except Exception:
        return None
