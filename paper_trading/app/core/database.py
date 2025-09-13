import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.connection_params = {
            'host': settings.db_host,
            'database': settings.db_name,
            'user': settings.db_user,
            'password': settings.db_password,
            'port': settings.db_port
        }

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params)
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()

    @contextmanager
    def get_cursor(self, dict_cursor=True):
        """Context manager for database cursors"""
        with self.get_connection() as conn:
            cursor_class = RealDictCursor if dict_cursor else None
            cursor = conn.cursor(cursor_factory=cursor_class)
            try:
                yield cursor, conn
                conn.commit()
            except Exception as e:
                conn.rollback()
                logger.error(f"Database operation error: {e}")
                raise
            finally:
                cursor.close()

    def init_database(self):
        """Initialize database tables"""
        create_tables_sql = """
        -- Trades table
        CREATE TABLE IF NOT EXISTS trades (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(10) NOT NULL,
            trade_type VARCHAR(4) CHECK (trade_type IN ('BUY', 'SELL')),
            quantity INTEGER NOT NULL,
            price DECIMAL(10, 4) NOT NULL,
            trade_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            portfolio_id VARCHAR(50) DEFAULT 'default',
            status VARCHAR(10) DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'CLOSED'))
        );

        -- Positions table
        CREATE TABLE IF NOT EXISTS positions (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(10) NOT NULL,
            net_quantity INTEGER NOT NULL,
            avg_price DECIMAL(10, 4) NOT NULL,
            total_invested DECIMAL(15, 4) NOT NULL,
            portfolio_id VARCHAR(50) DEFAULT 'default',
            last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(symbol, portfolio_id)
        );

        -- Portfolio table
        CREATE TABLE IF NOT EXISTS portfolio (
            id SERIAL PRIMARY KEY,
            portfolio_id VARCHAR(50) NOT NULL,
            cash_balance DECIMAL(15, 4) DEFAULT 100000.00,
            total_value DECIMAL(15, 4) DEFAULT 100000.00,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(portfolio_id)
        );

        -- Insert default portfolio
        INSERT INTO portfolio (portfolio_id, cash_balance, total_value)
        VALUES ('default', %s, %s)
        ON CONFLICT (portfolio_id) DO NOTHING;
        """

        with self.get_cursor() as (cursor, conn):
            cursor.execute(create_tables_sql, (settings.default_cash_balance, settings.default_cash_balance))

# Global database instance
db_manager = DatabaseManager()
