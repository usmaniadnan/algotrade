import yfinance as yf
from typing import Optional, Dict, List
import logging
from app.core.exceptions import PriceNotAvailableException

logger = logging.getLogger(__name__)

class PriceService:
    @staticmethod
    def get_current_price(symbol: str) -> float:
        """Get current price for a symbol"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d", interval="1m")
            if not data.empty:
                price = float(data['Close'].iloc[-1])
                logger.info(f"Fetched price for {symbol}: {price}")
                return price
            else:
                raise PriceNotAvailableException(symbol)
        except Exception as e:
            logger.error(f"Error fetching price for {symbol}: {e}")
            raise PriceNotAvailableException(symbol)

    @staticmethod
    def get_multiple_prices(symbols: List[str]) -> Dict[str, float]:
        """Get current prices for multiple symbols"""
        prices = {}
        failed_symbols = []

        for symbol in symbols:
            try:
                price = PriceService.get_current_price(symbol)
                prices[symbol] = price
            except PriceNotAvailableException:
                failed_symbols.append(symbol)
                logger.warning(f"Failed to fetch price for {symbol}")

        if failed_symbols:
            logger.warning(f"Failed to fetch prices for symbols: {failed_symbols}")

        return prices
