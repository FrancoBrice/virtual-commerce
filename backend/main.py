from fastapi import FastAPI
from api.endpoints import cart, stock
from fastapi.middleware.cors import CORSMiddleware
from models.database import Base, engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text

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

app.include_router(cart.router)
app.include_router(stock.router)
