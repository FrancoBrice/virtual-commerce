from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base
from math import floor

class CartProductAssociation(Base):
    __tablename__ = "cart_product_association"

    cart_id = Column(Integer, ForeignKey("cart.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    quantity = Column(Integer, nullable=False, default=1)  # Cantidad solicitada

    product = relationship("Product")

class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    products = relationship("CartProductAssociation", backref="cart")
    total = Column(Float, default=0.0)
    discounted_total = Column(Float, default=0.0)

    def calculate_total(self):
        self.total = sum(item.product.price * item.quantity for item in self.products)
        self.discounted_total = sum(
            (item.product.price * item.quantity) * (1 - (item.product.discountPercentage / 100))
            for item in self.products
        )

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    discount_percentage = Column(Float, default=0.0) 
    thumbnail = Column(String)
    rating = Column(Float, nullable=False, default=0.0)
    weight = Column(Float, nullable=True)
    width = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    depth = Column(Float, nullable=True)

    @property
    def stock_real(self):
        return floor(self.stock / self.rating) if self.rating > 0 else 0