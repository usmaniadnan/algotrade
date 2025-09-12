from sqlalchemy.orm import Session
from . import models, schemas

def get_position_by_symbol(db: Session, symbol: str):
    return db.query(models.Position).filter(models.Position.symbol == symbol).first()

def create_trade(db: Session, trade: schemas.TradeCreate):
    position = get_position_by_symbol(db, trade.symbol)

    if trade.trade_type == "sell":
        if not position or position.quantity < trade.quantity:
            return None # Invalid trade

    db_trade = models.Trade(**trade.dict())
    db.add(db_trade)

    if position:
        if trade.trade_type == "buy":
            new_quantity = position.quantity + trade.quantity
            new_average_price = ((position.average_price * position.quantity) + (trade.price * trade.quantity)) / new_quantity
            position.quantity = new_quantity
            position.average_price = new_average_price
        else: # sell
            position.quantity -= trade.quantity
    else:
        if trade.trade_type == "buy":
            position = models.Position(
                symbol=trade.symbol,
                quantity=trade.quantity,
                average_price=trade.price
            )
            db.add(position)

    db.commit()
    db.refresh(db_trade)
    return db_trade

def get_positions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Position).offset(skip).limit(limit).all()
