from fastapi import FastAPI
from api.endpoints import cart, stock, shipping
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
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1")) 
    Base.metadata.create_all(bind=engine)
    
except OperationalError:
    print("❌ Error: Database is not available. Tables not created.")
    

@app.on_event("startup")
async def startup_event():
    print("🚀 Poblando la base de datos con productos...")
    await populate_products()
    print("✅ Productos insertados en la base de datos.")


app.include_router(cart.router)
app.include_router(stock.router)
app.include_router(shipping.router)
