from fastapi import Depends, HTTPException
from app.services.trading_service import TradingService
from app.services.portfolio_service import PortfolioService
from app.services.price_service import PriceService

def get_trading_service() -> TradingService:
    return TradingService()

def get_portfolio_service() -> PortfolioService:
    return PortfolioService()

def get_price_service() -> PriceService:
    return PriceService()
