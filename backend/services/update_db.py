import httpx
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.models import Product

async def update_products():
    url = "https://dummyjson.com/products"
    limit = 10
    skip = 0

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params={"limit": 1, "skip": 0})
        response.raise_for_status()
        total = response.json().get("total", 0)  

        while skip < total:
            try:
                response = await client.get(url, params={"limit": limit, "skip": skip})
                response.raise_for_status()
                data = response.json()

                if "products" not in data:
                    break  

                with SessionLocal() as session:
                    for product in data["products"]:
                        product_data = {
                            "id": product["id"],
                            "title": product["title"],
                            "description": product.get("description", ""),
                            "price": product["price"],
                            "stock": product["stock"],
                            "discount_percentage": product.get("discountPercentage"),
                            "thumbnail": product["thumbnail"],
                            "rating": product.get("rating"),
                            "weight": product.get("weight"),
                            "width": product.get("dimensions", {}).get("width"),
                            "height": product.get("dimensions", {}).get("height"),
                            "depth": product.get("dimensions", {}).get("depth"),
                        }
                        session.merge(Product(**product_data))  
                    session.commit()

                skip += limit  # Aumenta el offset

            except httpx.HTTPStatusError as e:
                print(f"Error HTTP al obtener productos: {e.response.status_code} - {e.response.text}")
                break
            except httpx.RequestError as e:
                print(f"Error de conexión: {e}")
                break
            except Exception as e:
                print(f"Error inesperado: {e}")
                break
