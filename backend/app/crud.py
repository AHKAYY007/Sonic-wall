from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import model, schemas

# ---------- Stats ----------

def get_average_latency(db: Session) -> float:
    """
    Calculate average latency in milliseconds between call_time and confirmed_at.
    Uses SQLite-compatible timestamp difference.
    """
    latency = db.query(
        func.avg(
            func.strftime('%s', model.ContractCall.confirmed_at) -
            func.strftime('%s', model.ContractCall.call_time)
        )
    ).scalar()
    return round(latency * 1000, 2) if latency else 0


def get_stats(db: Session) -> dict:
    """
    Get overall stats: total calls, blocked percentage, and average latency.
    """
    total = db.query(func.count(model.ContractCall.id)).scalar()
    blocked = db.query(func.count(model.BlockedAddress.id)).scalar()
    avg_latency = get_average_latency(db)

    return {
        "totalCalls": total,
        "blockedPercentage": round((blocked / (total + 1)) * 100, 2),  # Avoid divide-by-zero
        "averageLatencyMs": avg_latency
    }

# ---------- Traffic ----------

def get_traffic(db: Session, limit: int = 10):
    """
    Fetch recent contract calls ordered by most recent.
    """
    return (
        db.query(model.ContractCall)
        .order_by(model.ContractCall.call_time.desc())
        .limit(limit)
        .all()
    )


def create_call(db: Session, call: schemas.ContractCallCreate):
    """
    Create a new contract call entry.
    """
    db_call = model.ContractCall(**call.dict())
    db.add(db_call)
    db.commit()
    db.refresh(db_call)
    return db_call


def confirm_call(db: Session, call_id: int):
    """
    Mark a contract call as confirmed with the current timestamp.
    """
    call = db.query(model.ContractCall).filter_by(id=call_id).first()
    if call:
        call.confirmed_at = datetime.utcnow()
        db.commit()
        db.refresh(call)
    return call

# ---------- Blocking ----------

def get_blocked(db: Session):
    """
    Retrieve all blocked addresses.
    """
    return db.query(model.BlockedAddress).all()


def block_address(db: Session, address: str):
    """
    Block an address if it's not already blocked.
    """
    if not db.query(model.BlockedAddress).filter_by(address=address).first():
        blocked = model.BlockedAddress(address=address)
        db.add(blocked)
        db.commit()
        db.refresh(blocked)
        return blocked
    return {"message": "Address already blocked"}


def unblock_address(db: Session, addr: str):
    """
    Unblock an address if it exists.
    """
    obj = db.query(model.BlockedAddress).filter_by(address=addr).first()
    if obj:
        db.delete(obj)
        db.commit()
        return {"unblocked": addr}
    return {"message": "Address not found"}
