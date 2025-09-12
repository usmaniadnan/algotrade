from pydantic import BaseModel
from datetime import datetime

class TradeBase(BaseModel):
    symbol: str
    quantity: int
    price: float
    trade_type: str

class TradeCreate(TradeBase):
    pass

class Trade(TradeBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class PositionBase(BaseModel):
    symbol: str
    quantity: int
    average_price: float

class Position(PositionBase):
    id: int

    class Config:
        orm_mode = True
