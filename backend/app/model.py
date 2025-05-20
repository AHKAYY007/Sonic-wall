from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from datetime import datetime

class ContractCall(Base):
    __tablename__ = "contract_calls"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    sender = Column(String)
    address = Column(String)
    method = Column(String)

class BlockedAddress(Base):
    __tablename__ = "blocked_addresses"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True)
    reason = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)