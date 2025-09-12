from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    quantity = Column(Integer)
    price = Column(Float)
    trade_type = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    quantity = Column(Integer)
    average_price = Column(Float)
