from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal
from decimal import Decimal

class TradeCreate(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=10, description="Stock symbol")
    trade_type: Literal["BUY", "SELL"] = Field(..., description="Trade type")
    quantity: int = Field(..., gt=0, description="Number of shares")
    price: Optional[float] = Field(None, gt=0, description="Price per share (optional, will fetch current if not provided)")
    portfolio_id: str = Field("default", description="Portfolio ID")

class TradeResponse(BaseModel):
    id: int
    symbol: str
    trade_type: str
    quantity: int
    price: Decimal
    trade_date: datetime
    portfolio_id: str
    status: str

class TradeHistory(BaseModel):
    trades: list[TradeResponse]
    total_count: int
    page: int
    page_size: int
