import httpx
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.models import Product

async def populate_products():
    url = "https://dummyjson.com/products"
    limit = 10
    skip = 0

    async with httpx.AsyncClient() as client:
        while True:
            try:
                response = await client.get(url, params={"limit": limit, "skip": skip})
                response.raise_for_status()
                data = response.json()

                with SessionLocal() as session:
                    for product in data.get("products", []):
                        existing_product = session.query(Product).filter_by(id=product["id"]).first()

                        if existing_product:
                            existing_product.title = product["title"]
                            existing_product.description = product.get("description", "")
                            existing_product.price = product["price"]
                            existing_product.stock = product["stock"]
                            existing_product.discount_percentage = product.get("discountPercentage")
                            existing_product.thumbnail = product["thumbnail"]
                            existing_product.rating = product.get("rating")
                            existing_product.weight = product.get("weight")
                            existing_product.width = product["dimensions"]["width"]
                            existing_product.height = product["dimensions"]["height"]
                            existing_product.depth = product["dimensions"]["depth"]
                        else:
                            new_product = Product(
                                id=product["id"],
                                title=product["title"],
                                description=product.get("description", ""),
                                price=product["price"],
                                stock=product["stock"],
                                discount_percentage=product.get("discountPercentage"),
                                thumbnail=product["thumbnail"],
                                rating=product.get("rating"),
                                weight=product.get("weight"),
                                width=product["dimensions"]["width"],
                                height=product["dimensions"]["height"],
                                depth=product["dimensions"]["depth"],
                            )
                            session.add(new_product)

                    session.commit()

                total = data.get("total", 0)
                if skip + limit >= total:
                    break

                skip += limit

            except httpx.HTTPStatusError as e:
                print(f"Error HTTP al obtener productos: {e.response.status_code} - {e.response.text}")
                break
            except httpx.RequestError as e:
                print(f"Error de conexión: {e}")
                break
            except Exception as e:
                print(f"Error inesperado: {e}")
                break
