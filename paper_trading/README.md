# Paper Trading API

A comprehensive REST API for paper trading with PostgreSQL backend, built with FastAPI.

## Features

- **Trade Management**: Place BUY/SELL orders with real-time price fetching
- **Portfolio Tracking**: Monitor cash balance and total portfolio value
- **Position Management**: Track positions with average cost and P&L
- **Real-time P&L**: Calculate current profit/loss using live market data
- **REST API**: Complete API with OpenAPI documentation
- **Database**: PostgreSQL with proper schema and relationships

## Quick Start

### 1. Setup Environment

```bash
# Clone the repository (create the directory structure as shown above)
mkdir paper_trading && cd paper_trading

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Using Docker (recommended)
docker-compose up -d postgres

# Or install PostgreSQL manually and create database
createdb paper_trading
```

### 3. Configuration

Update `.env` file with your database credentials:

```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=paper_trading
DB_USER=postgres
DB_PASSWORD=your_password
```

### 4. Run the Application

```bash
# Using the run script
python run.py

# Or using uvicorn directly
uvicorn app.main:app --reload
```

The API will be available at: http://localhost:8000

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Trades
- `POST /api/v1/trades/` - Place a new trade
- `GET /api/v1/trades/` - Get trade history (paginated)
- `GET /api/v1/trades/{trade_id}` - Get specific trade

### Portfolio
- `GET /api/v1/portfolio/` - Get portfolio overview
- `GET /api/v1/portfolio/pnl` - Get portfolio P&L with live prices
- `PUT /api/v1/portfolio/cash` - Update cash balance

### Positions
- `GET /api/v1/positions/` - Get all positions
- `GET /api/v1/positions/{symbol}` - Get specific position
- `DELETE /api/v1/positions/{symbol}` - Close position

### Prices
- `GET /api/v1/prices/{symbol}` - Get current price for symbol
- `POST /api/v1/prices/bulk` - Get prices for multiple symbols

## Example Usage

### Place a Trade
```bash
curl -X POST "http://localhost:8000/api/v1/trades/" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "trade_type": "BUY",
    "quantity": 10
  }'
```

### Get Portfolio P&L
```bash
curl "http://localhost:8000/api/v1/portfolio/pnl"
```

### Get Current Price
```bash
curl "http://localhost:8000/api/v1/prices/AAPL"
```

## Development

### Running Tests
```bash
pytest tests/
```

### Database Migrations
The application automatically creates necessary tables on startup.

## Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## Project Structure

```
paper_trading/
├── app/
│   ├── api/routes/          # API route handlers
│   ├── core/               # Core configuration and database
│   ├── models/             # Pydantic models
│   ├── services/           # Business logic services
│   └── utils/              # Utility functions
├── tests/                  # Test files
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables
└── docker-compose.yml     # Docker configuration
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License
