from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/trades/", response_model=schemas.Trade)
def create_trade_api(trade: schemas.TradeCreate, db: Session = Depends(get_db)):
    db_trade = crud.create_trade(db=db, trade=trade)
    if db_trade is None:
        raise HTTPException(status_code=400, detail="Invalid trade")
    return db_trade

@app.get("/positions/", response_model=list[schemas.Position])
def read_positions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    positions = crud.get_positions(db, skip=skip, limit=limit)
    return positions
