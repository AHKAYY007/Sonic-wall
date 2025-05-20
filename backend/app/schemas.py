from pydantic import BaseModel
from datetime import datetime

# Input schema for creating contract calls
class ContractCallCreate(BaseModel):
    sender: str
    address: str
    method: str

# Output schema
class ContractCallOut(ContractCallCreate):
    timestamp: datetime
    class Config:
        orm_mode = True

# Blocked address input
class BlockedAddressBase(BaseModel):
    address: str

# Output
class BlockedAddressOut(BlockedAddressBase):
    id: int
    class Config:
        orm_mode = True
