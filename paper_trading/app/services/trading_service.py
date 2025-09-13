from typing import Optional, List, Dict
from decimal import Decimal
import logging
from app.core.database import db_manager
from app.core.exceptions import (
    InsufficientFundsException,
    InsufficientSharesException,
    PortfolioNotFoundException
)
from app.services.price_service import PriceService
from app.models.trade import TradeCreate, TradeResponse

logger = logging.getLogger(__name__)

class TradingService:
    def __init__(self):
        self.price_service = PriceService()

    def place_trade(self, trade: TradeCreate) -> TradeResponse:
        """Place a new trade"""
        # Get current price if not provided
        price = trade.price or self.price_service.get_current_price(trade.symbol)
        trade_value = price * trade.quantity

        with db_manager.get_cursor() as (cursor, conn):
            # Verify portfolio exists
            cursor.execute(
                "SELECT cash_balance FROM portfolio WHERE portfolio_id = %s",
                (trade.portfolio_id,)
            )
            portfolio_result = cursor.fetchone()
            if not portfolio_result:
                raise PortfolioNotFoundException(trade.portfolio_id)

            cash_balance = float(portfolio_result['cash_balance'])

            # Validate trade
            if trade.trade_type == 'BUY':
                if cash_balance < trade_value:
                    raise InsufficientFundsException(
                        f"Required: ${trade_value:.2f}, Available: ${cash_balance:.2f}"
                    )
            else:  # SELL
                # Check if sufficient shares available
                cursor.execute("""
                    SELECT net_quantity FROM positions
                    WHERE symbol = %s AND portfolio_id = %s
                """, (trade.symbol, trade.portfolio_id))
                position_result = cursor.fetchone()

                available_shares = position_result['net_quantity'] if position_result else 0
                if available_shares < trade.quantity:
                    raise InsufficientSharesException(
                        f"Required: {trade.quantity}, Available: {available_shares}"
                    )

            # Insert trade
            cursor.execute("""
                INSERT INTO trades (symbol, trade_type, quantity, price, portfolio_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, symbol, trade_type, quantity, price, trade_date, portfolio_id, status
            """, (trade.symbol, trade.trade_type, trade.quantity, price, trade.portfolio_id))

            trade_result = cursor.fetchone()

            # Update positions
            self._update_position(cursor, trade.symbol, trade.trade_type,
                                trade.quantity, price, trade.portfolio_id)

            # Update cash balance
            cash_change = -trade_value if trade.trade_type == 'BUY' else trade_value
            cursor.execute("""
                UPDATE portfolio
                SET cash_balance = cash_balance + %s, updated_at = CURRENT_TIMESTAMP
                WHERE portfolio_id = %s
            """, (cash_change, trade.portfolio_id))

            logger.info(f"Trade executed: {trade.trade_type} {trade.quantity} {trade.symbol} @ {price}")

            return TradeResponse(**trade_result)

    def _update_position(self, cursor, symbol: str, trade_type: str,
                        quantity: int, price: float, portfolio_id: str):
        """Update position after trade"""
        cursor.execute("""
            SELECT net_quantity, avg_price, total_invested
            FROM positions WHERE symbol = %s AND portfolio_id = %s
        """, (symbol, portfolio_id))

        result = cursor.fetchone()

        if result:
            current_qty = result['net_quantity']
            current_avg_price = float(result['avg_price'])
            current_invested = float(result['total_invested'])

            if trade_type == 'BUY':
                new_qty = current_qty + quantity
                new_invested = current_invested + (price * quantity)
                new_avg_price = new_invested / new_qty if new_qty > 0 else 0
            else:  # SELL
                new_qty = current_qty - quantity
                if new_qty > 0:
                    new_invested = current_invested * (new_qty / current_qty)
                    new_avg_price = current_avg_price
                else:
                    new_invested = 0
                    new_avg_price = 0

            if new_qty == 0:
                cursor.execute("""
                    DELETE FROM positions WHERE symbol = %s AND portfolio_id = %s
                """, (symbol, portfolio_id))
            else:
                cursor.execute("""
                    UPDATE positions
                    SET net_quantity = %s, avg_price = %s, total_invested = %s,
                        last_updated = CURRENT_TIMESTAMP
                    WHERE symbol = %s AND portfolio_id = %s
                """, (new_qty, new_avg_price, new_invested, symbol, portfolio_id))
        else:
            # New position (only for BUY)
            if trade_type == 'BUY':
                cursor.execute("""
                    INSERT INTO positions (symbol, net_quantity, avg_price, total_invested, portfolio_id)
                    VALUES (%s, %s, %s, %s, %s)
                """, (symbol, quantity, price, price * quantity, portfolio_id))

    def get_trade_history(self, portfolio_id: str = "default",
                         page: int = 1, page_size: int = 50) -> Dict:
        """Get trade history with pagination"""
        offset = (page - 1) * page_size

        with db_manager.get_cursor() as (cursor, conn):
            # Get total count
            cursor.execute("""
                SELECT COUNT(*) as total FROM trades WHERE portfolio_id = %s
            """, (portfolio_id,))
            total_count = cursor.fetchone()['total']

            # Get trades
            cursor.execute("""
                SELECT id, symbol, trade_type, quantity, price, trade_date, portfolio_id, status
                FROM trades
                WHERE portfolio_id = %s
                ORDER BY trade_date DESC
                LIMIT %s OFFSET %s
            """, (portfolio_id, page_size, offset))

            trades = [TradeResponse(**row) for row in cursor.fetchall()]

            return {
                "trades": trades,
                "total_count": total_count,
                "page": page,
                "page_size": page_size
            }

    def get_trade_by_id(self, trade_id: int) -> Optional[TradeResponse]:
        """Get specific trade by ID"""
        with db_manager.get_cursor() as (cursor, conn):
            cursor.execute("""
                SELECT id, symbol, trade_type, quantity, price, trade_date, portfolio_id, status
                FROM trades WHERE id = %s
            """, (trade_id,))

            result = cursor.fetchone()
            return TradeResponse(**result) if result else None
