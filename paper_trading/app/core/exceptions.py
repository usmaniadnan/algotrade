from fastapi import HTTPException

class TradingException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)

class InsufficientFundsException(TradingException):
    def __init__(self, detail: str = "Insufficient cash balance"):
        super().__init__(detail=detail, status_code=400)

class InsufficientSharesException(TradingException):
    def __init__(self, detail: str = "Insufficient shares to sell"):
        super().__init__(detail=detail, status_code=400)

class PriceNotAvailableException(TradingException):
    def __init__(self, symbol: str):
        super().__init__(detail=f"Price not available for symbol: {symbol}", status_code=400)

class PortfolioNotFoundException(TradingException):
    def __init__(self, portfolio_id: str):
        super().__init__(detail=f"Portfolio not found: {portfolio_id}", status_code=404)

class TradeNotFoundException(TradingException):
    def __init__(self, trade_id: int):
        super().__init__(detail=f"Trade not found: {trade_id}", status_code=404)
