import json 
from models.database import SessionLocal

def print_cart(cart_data): 
  print(json.dumps(cart_data, indent=4, ensure_ascii=False))

def get_db():
    db = SessionLocal()
    try:
        yield db  # Proporciona la sesión a la ruta
    finally:
        db.close() 