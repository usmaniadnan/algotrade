from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class PositionResponse(BaseModel):
    symbol: str
    net_quantity: int
    avg_price: Decimal
    total_invested: Decimal
    last_updated: datetime
    portfolio_id: str

class PriceResponse(BaseModel):
    symbol: str
    price: float
    timestamp: datetime

class BulkPriceRequest(BaseModel):
    symbols: list[str]

class BulkPriceResponse(BaseModel):
    prices: dict[str, float]
    timestamp: datetime
