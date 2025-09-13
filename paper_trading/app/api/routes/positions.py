from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from datetime import datetime
from app.models.position import PositionResponse, PriceResponse, BulkPriceRequest, BulkPriceResponse
from app.services.portfolio_service import PortfolioService
from app.services.price_service import PriceService
from app.api.dependencies import get_portfolio_service, get_price_service

router = APIRouter()

@router.get("/positions/", response_model=List[PositionResponse])
async def get_positions(
    portfolio_id: str = Query("default", description="Portfolio ID"),
    portfolio_service: PortfolioService = Depends(get_portfolio_service)
):
    """Get all current positions"""
    try:
        return portfolio_service.get_positions(portfolio_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/positions/{symbol}", response_model=PositionResponse)
async def get_position(
    symbol: str,
    portfolio_id: str = Query("default", description="Portfolio ID"),
    portfolio_service: PortfolioService = Depends(get_portfolio_service)
):
    """Get specific position by symbol"""
    try:
        position = portfolio_service.get_position_by_symbol(symbol, portfolio_id)
        if not position:
            raise HTTPException(status_code=404, detail=f"Position not found for symbol: {symbol}")
        return position
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/positions/{symbol}")
async def close_position(
    symbol: str,
    portfolio_id: str = Query("default", description="Portfolio ID"),
    portfolio_service: PortfolioService = Depends(get_portfolio_service)
):
    """Close entire position for a symbol"""
    try:
        success = portfolio_service.close_position(symbol, portfolio_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Position not found or could not be closed: {symbol}")
        return {"message": f"Position for {symbol} closed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/prices/{symbol}", response_model=PriceResponse)
async def get_price(
    symbol: str,
    price_service: PriceService = Depends(get_price_service)
):
    """Get current price for a symbol"""
    try:
        price = price_service.get_current_price(symbol)
        return PriceResponse(symbol=symbol, price=price, timestamp=datetime.now())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/prices/bulk", response_model=BulkPriceResponse)
async def get_bulk_prices(
    request: BulkPriceRequest,
    price_service: PriceService = Depends(get_price_service)
):
    """Get current prices for multiple symbols"""
    try:
        prices = price_service.get_multiple_prices(request.symbols)
        return BulkPriceResponse(prices=prices, timestamp=datetime.now())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
