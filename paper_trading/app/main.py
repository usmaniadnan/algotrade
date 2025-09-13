from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import db_manager
from app.api.routes import trades, portfolio, positions
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Paper Trading API",
    description="A REST API for paper trading with PostgreSQL backend",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(trades.router, prefix="/api/v1", tags=["Trades"])
app.include_router(portfolio.router, prefix="/api/v1", tags=["Portfolio"])
app.include_router(positions.router, prefix="/api/v1", tags=["Positions"])

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        db_manager.init_database()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Paper Trading API is running"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Paper Trading API",
        "docs": "/docs",
        "redoc": "/redoc"
    }
