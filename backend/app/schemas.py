from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# ---------- Contract Call ----------

class ContractCallCreate(BaseModel):
    from_address: str
    to_address: str
    method: str

class ContractCallOut(BaseModel):
    id: int
    from_address: str
    to_address: str
    method: str
    call_time: datetime
    confirmed_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


# ---------- Blocked Address ----------

class BlockedAddressBase(BaseModel):
    address: str

class BlockedAddressOut(BaseModel):
    id: int
    address: str

    model_config = ConfigDict(from_attributes=True)
