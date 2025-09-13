from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from app.models.trade import TradeCreate, TradeResponse, TradeHistory
from app.services.trading_service import TradingService
from app.api.dependencies import get_trading_service
from app.core.exceptions import TradeNotFoundException

router = APIRouter()

@router.post("/trades/", response_model=TradeResponse)
async def place_trade(
    trade: TradeCreate,
    trading_service: TradingService = Depends(get_trading_service)
):
    """Place a new trade"""
    try:
        return trading_service.place_trade(trade)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/trades/", response_model=TradeHistory)
async def get_trade_history(
    portfolio_id: str = Query("default", description="Portfolio ID"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    trading_service: TradingService = Depends(get_trading_service)
):
    """Get trade history with pagination"""
    try:
        history_data = trading_service.get_trade_history(portfolio_id, page, page_size)
        return TradeHistory(**history_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/trades/{trade_id}", response_model=TradeResponse)
async def get_trade(
    trade_id: int,
    trading_service: TradingService = Depends(get_trading_service)
):
    """Get specific trade by ID"""
    trade = trading_service.get_trade_by_id(trade_id)
    if not trade:
        raise TradeNotFoundException(trade_id)
    return trade
