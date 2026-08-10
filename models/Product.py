from pydantic import BaseModel
from typing import Optional

class ProductSchema(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    price: float
    quantity: int


from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# SQLAlchemy Model
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True) #Index makes it faster to search for items
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float)
    quantity = Column(Integer)