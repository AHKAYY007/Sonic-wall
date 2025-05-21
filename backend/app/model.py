from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ContractCall(Base):
    __tablename__ = "contract_calls"

    id = Column(Integer, primary_key=True, index=True)
    from_address = Column(String, index=True)
    to_address = Column(String, index=True)
    method = Column(String)
    call_time = Column(DateTime, default=datetime.utcnow)
    confirmed_at = Column(DateTime, nullable=True)

class BlockedAddress(Base):
    __tablename__ = "blocked_addresses"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, index=True)
