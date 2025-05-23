from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import model, schemas
import requests

# ---------- Config ----------
SONICSCAN_API_KEY = "EE19MS8ZX5XJRVCBQR5RJT1QEQR3CUV7KM"
SONICSCAN_API_URL = "https://api.sonicscan.org/api"

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


def get_blocked_address(db: Session, addr: str):
    """
    Retrieve a blocked address by its address.
    """
    obj = db.query(model.BlockedAddress).filter_by(address=addr).first()
    return obj if obj else {"message": "Address not found"}


def is_blocked(db: Session, addr: str):
    """
    Check if an address is blocked.
    """
    obj = db.query(model.BlockedAddress).filter_by(address=addr).first()
    return {"blocked": bool(obj)}


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

# ---------- Wallet: Local ----------

def get_wallet_history(db: Session, address: str, limit: int = 20):
    """
    Retrieve recent contract calls involving the given wallet address (from or to).
    """
    return (
        db.query(model.ContractCall)
        .filter(
            (model.ContractCall.from_address == address) |
            (model.ContractCall.to_address == address)
        )
        .order_by(model.ContractCall.call_time.desc())
        .limit(limit)
        .all()
    )


def get_wallet_transactions(db: Session, address: str):
    """
    Retrieve all transactions sent from a given wallet address.
    """
    return (
        db.query(model.ContractCall)
        .filter_by(from_address=address)
        .order_by(model.ContractCall.call_time.desc())
        .all()
    )

# ---------- Wallet: SonicScan Integration ----------

def fetch_wallet_transactions(wallet_address: str) -> list:
    """
    Fetch transactions for a given wallet address from SonicScan.
    """
    params = {
        "module": "account",
        "action": "txlist",
        "address": wallet_address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc",
        "apikey": SONICSCAN_API_KEY
    }
    response = requests.get(SONICSCAN_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "1":
            return data.get("result", [])
    return []


def sync_wallet_transactions(db: Session, wallet_address: str):
    """
    Sync transactions from SonicScan to the local database.
    """
    transactions = fetch_wallet_transactions(wallet_address)

    for tx in transactions:
        call_time = datetime.fromtimestamp(int(tx["timeStamp"]))
        exists = db.query(model.ContractCall).filter_by(
            from_address=tx["from"],
            to_address=tx["to"],
            call_time=call_time
        ).first()

        if not exists:
            new_call = model.ContractCall(
                from_address=tx["from"],
                to_address=tx["to"],
                method=tx.get("functionName", "unknown"),
                call_time=call_time,
                confirmed_at=call_time if tx.get("timeStamp") else None
            )
            db.add(new_call)

    db.commit()
