from typing import List, Dict
from datetime import datetime
import logging
from app.core.database import db_manager
from app.core.exceptions import PortfolioNotFoundException
from app.services.price_service import PriceService
from app.models.portfolio import PortfolioResponse, PortfolioPnL, PositionPnL
from app.models.position import PositionResponse

logger = logging.getLogger(__name__)

class PortfolioService:
    def __init__(self):
        self.price_service = PriceService()

    def get_portfolio(self, portfolio_id: str = "default") -> PortfolioResponse:
        """Get portfolio details"""
        with db_manager.get_cursor() as (cursor, conn):
            cursor.execute("""
                SELECT portfolio_id, cash_balance, total_value, created_at, updated_at
                FROM portfolio WHERE portfolio_id = %s
            """, (portfolio_id,))

            result = cursor.fetchone()
            if not result:
                raise PortfolioNotFoundException(portfolio_id)

            return PortfolioResponse(**result)

    def get_positions(self, portfolio_id: str = "default") -> List[PositionResponse]:
        """Get all positions for a portfolio"""
        with db_manager.get_cursor() as (cursor, conn):
            cursor.execute("""
                SELECT symbol, net_quantity, avg_price, total_invested, last_updated, portfolio_id
                FROM positions
                WHERE portfolio_id = %s AND net_quantity > 0
                ORDER BY symbol
            """, (portfolio_id,))

            positions = [PositionResponse(**row) for row in cursor.fetchall()]
            return positions

    def get_position_by_symbol(self, symbol: str, portfolio_id: str = "default") -> PositionResponse:
        """Get specific position by symbol"""
        with db_manager.get_cursor() as (cursor, conn):
            cursor.execute("""
                SELECT symbol, net_quantity, avg_price, total_invested, last_updated, portfolio_id
                FROM positions
                WHERE symbol = %s AND portfolio_id = %s
            """, (symbol, portfolio_id))

            result = cursor.fetchone()
            if not result:
                return None

            return PositionResponse(**result)

    def get_portfolio_pnl(self, portfolio_id: str = "default") -> PortfolioPnL:
        """Calculate portfolio P&L with current prices"""
        positions = self.get_positions(portfolio_id)

        if not positions:
            cash_balance = self._get_cash_balance(portfolio_id)
            return PortfolioPnL(
                portfolio_id=portfolio_id,
                cash_balance=cash_balance,
                total_invested=0,
                current_value=0,
                total_pnl=0,
                total_portfolio_value=cash_balance,
                positions_pnl=[]
            )

        # Get current prices for all symbols
        symbols = [pos.symbol for pos in positions]
        current_prices = self.price_service.get_multiple_prices(symbols)

        positions_pnl = []
        total_pnl = 0
        total_invested = 0
        current_portfolio_value = 0

        for position in positions:
            symbol = position.symbol
            quantity = position.net_quantity
            avg_price = float(position.avg_price)
            invested = float(position.total_invested)

            current_price = current_prices.get(symbol, avg_price)
            current_value = current_price * quantity
            pnl = current_value - invested
            pnl_percent = (pnl / invested) * 100 if invested > 0 else 0

            position_pnl = PositionPnL(
                symbol=symbol,
                quantity=quantity,
                avg_price=avg_price,
                current_price=current_price,
                invested=invested,
                current_value=current_value,
                pnl=pnl,
                pnl_percent=pnl_percent
            )

            positions_pnl.append(position_pnl)
            total_pnl += pnl
            total_invested += invested
            current_portfolio_value += current_value

        cash_balance = self._get_cash_balance(portfolio_id)

        return PortfolioPnL(
            portfolio_id=portfolio_id,
            cash_balance=cash_balance,
            total_invested=total_invested,
            current_value=current_portfolio_value,
            total_pnl=total_pnl,
            total_portfolio_value=current_portfolio_value + cash_balance,
            positions_pnl=positions_pnl
        )

    def update_cash_balance(self, portfolio_id: str, new_balance: float) -> PortfolioResponse:
        """Update portfolio cash balance"""
        with db_manager.get_cursor() as (cursor, conn):
            cursor.execute("""
                UPDATE portfolio
                SET cash_balance = %s, updated_at = CURRENT_TIMESTAMP
                WHERE portfolio_id = %s
                RETURNING portfolio_id, cash_balance, total_value, created_at, updated_at
            """, (new_balance, portfolio_id))

            result = cursor.fetchone()
            if not result:
                raise PortfolioNotFoundException(portfolio_id)

            return PortfolioResponse(**result)

    def _get_cash_balance(self, portfolio_id: str) -> float:
        """Get current cash balance"""
        with db_manager.get_cursor() as (cursor, conn):
            cursor.execute(
                "SELECT cash_balance FROM portfolio WHERE portfolio_id = %s",
                (portfolio_id,)
            )
            result = cursor.fetchone()
            return float(result['cash_balance']) if result else 0

    def close_position(self, symbol: str, portfolio_id: str = "default") -> bool:
        """Close entire position for a symbol"""
        position = self.get_position_by_symbol(symbol, portfolio_id)
        if not position:
            return False

        # Create a SELL trade for the entire position
        from app.services.trading_service import TradingService
        from app.models.trade import TradeCreate

        trading_service = TradingService()
        sell_trade = TradeCreate(
            symbol=symbol,
            trade_type="SELL",
            quantity=position.net_quantity,
            portfolio_id=portfolio_id
        )

        try:
            trading_service.place_trade(sell_trade)
            return True
        except Exception as e:
            logger.error(f"Error closing position for {symbol}: {e}")
            return False
