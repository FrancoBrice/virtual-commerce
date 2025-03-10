import asyncio
from fastapi import FastAPI
from api.endpoints import cart, shipping
from fastapi.middleware.cors import CORSMiddleware
from models.database import Base, engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text 
from services.populate_db import populate_products

app = FastAPI(title="Flapp Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)


try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1")) 
    Base.metadata.create_all(bind=engine)
except OperationalError:
    print("Error: Database is not available. Tables not created.")

async def cron_job():
    while True:
        print("Running cron job: Populating the database with products...")
        await populate_products()
        print("Products inserted into the database.")
        await asyncio.sleep(86400)  # 1 day

@app.on_event("startup")
async def startup_event():
    print("Populating the database with products on startup...")
    await populate_products()
    print("Products inserted into the database.")
    asyncio.create_task(cron_job())

app.include_router(cart.router)
app.include_router(shipping.router)
