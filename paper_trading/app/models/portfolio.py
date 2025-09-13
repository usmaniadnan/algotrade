from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from decimal import Decimal

class PortfolioResponse(BaseModel):
    portfolio_id: str
    cash_balance: Decimal
    total_value: Decimal
    created_at: datetime
    updated_at: datetime

class PositionPnL(BaseModel):
    symbol: str
    quantity: int
    avg_price: Decimal
    current_price: Decimal
    invested: Decimal
    current_value: Decimal
    pnl: Decimal
    pnl_percent: float

class PortfolioPnL(BaseModel):
    portfolio_id: str
    cash_balance: Decimal
    total_invested: Decimal
    current_value: Decimal
    total_pnl: Decimal
    total_portfolio_value: Decimal
    positions_pnl: List[PositionPnL]

class CashBalanceUpdate(BaseModel):
    cash_balance: float = Field(..., gt=0, description="New cash balance")
