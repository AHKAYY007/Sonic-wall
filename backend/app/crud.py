from sqlalchemy.orm import Session
from . import model, schemas
from sqlalchemy import func

def get_stats(db: Session):
    total = db.query(func.count(model.ContractCall.id)).scalar()
    blocked = db.query(func.count(model.BlockedAddress.id)).scalar()
    return {
        "totalCalls": total,
        "blockedPercentage": round((blocked / (total + 1)) * 100, 2),  # avoids /0
        "averageLatencyMs": 204  # Replace with real calc later
    }

def get_traffic(db: Session, limit: int = 10):
    return db.query(model.ContractCall).order_by(model.ContractCall.timestamp.desc()).limit(limit).all()

def create_call(db: Session, call: schemas.ContractCallCreate):
    db_call = model.ContractCall(**call.dict())
    db.add(db_call)
    db.commit()
    db.refresh(db_call)
    return db_call

def get_blocked(db: Session):
    return db.query(model.BlockedAddress).all()

def block_address(db: Session, address: str):
    # Prevent duplicate blocks
    if not db.query(model.BlockedAddress).filter_by(address=address).first():
        blocked = model.BlockedAddress(address=address)
        db.add(blocked)
        db.commit()
        db.refresh(blocked)
        return blocked
    return {"message": "Address already blocked"}

def unblock_address(db: Session, addr: str):
    obj = db.query(model.BlockedAddress).filter_by(address=addr).first()
    if obj:
        db.delete(obj)
        db.commit()
        return {"unblocked": addr}
    return {"message": "Address not found"}
