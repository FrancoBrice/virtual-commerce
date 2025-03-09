import os
import requests
import json
from services.cart_service import get_cart

def get_best_shipping_rate():
    cart_data = get_cart()
    if not cart_data:
        return None

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

    traloya_price = get_courier_rate("TraeloYa", os.getenv("TRALEOYA_API_URL"), os.getenv("TRALEOYA_API_KEY"), waypoints, items)
    uder_price = get_courier_rate("Uder", os.getenv("UDER_API_URL"), os.getenv("UDER_API_KEY"), waypoints, items)

    shipping_options = []
    if traloya_price:
        shipping_options.append({"courier": "TraeloYa", "price": traloya_price})
    if uder_price:
        shipping_options.append({"courier": "Uder", "price": uder_price})

    return min(shipping_options, key=lambda x: x["price"]) if shipping_options else None



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
