from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.portfolio import PortfolioResponse, PortfolioPnL, CashBalanceUpdate
from app.services.portfolio_service import PortfolioService
from app.api.dependencies import get_portfolio_service

router = APIRouter()

@router.get("/portfolio/", response_model=PortfolioResponse)
async def get_portfolio(
    portfolio_id: str = Query("default", description="Portfolio ID"),
    portfolio_service: PortfolioService = Depends(get_portfolio_service)
):
    """Get portfolio overview"""
    try:
        return portfolio_service.get_portfolio(portfolio_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/portfolio/pnl", response_model=PortfolioPnL)
async def get_portfolio_pnl(
    portfolio_id: str = Query("default", description="Portfolio ID"),
    portfolio_service: PortfolioService = Depends(get_portfolio_service)
):
    """Get portfolio P&L with current market prices"""
    try:
        return portfolio_service.get_portfolio_pnl(portfolio_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/portfolio/cash", response_model=PortfolioResponse)
async def update_cash_balance(
    cash_update: CashBalanceUpdate,
    portfolio_id: str = Query("default", description="Portfolio ID"),
    portfolio_service: PortfolioService = Depends(get_portfolio_service)
):
    """Update portfolio cash balance"""
    try:
        return portfolio_service.update_cash_balance(portfolio_id, cash_update.cash_balance)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
