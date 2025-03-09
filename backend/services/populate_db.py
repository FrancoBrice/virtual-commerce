import httpx
from sqlalchemy.orm import Session
from models.database import SessionLocal, engine
from models.models import Product  # Importar el modelo de productos

async def populate_products():
    """
    Obtiene todos los productos desde la API de DummyJSON y los almacena en la base de datos.
    """
    url = "https://dummyjson.com/products"
    limit = 10
    skip = 0

    async with httpx.AsyncClient() as client:
        while True:
            response = await client.get(url, params={"limit": limit, "skip": skip})
            response.raise_for_status()
            data = response.json()

            # Abre una sesión con la base de datos
            with SessionLocal() as session:
                for product in data.get("products", []):
                    # Verificar si el producto ya existe en la base de datos
                    existing_product = session.query(Product).filter_by(id=product["id"]).first()
                    if not existing_product:
                        new_product = Product(
                            id=product["id"],
                            title=product["title"],
                            description=product["description"],
                            price=product["price"],
                            stock=product["stock"],
                            discountPercentage=product["discountPercentage"],
                            thumbnail=product["thumbnail"],
                            rating=product["rating"],
                        )
                        session.add(new_product)
                
                session.commit()  # Confirmar la transacción

            total = data.get("total", 0)
            if skip + limit >= total:
                break

            skip += limit
