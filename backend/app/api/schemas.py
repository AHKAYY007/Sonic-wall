from pydantic import BaseModel, Field
from app.api.types import AddressStr

# Base response for consistent messaging
class BaseResponse(BaseModel):
    message: str = Field(..., description="Response message", example="Address is blacklisted")
    status_code: int = Field(..., description="HTTP status code", example=200)
    error: str | None = Field(None, description="Error message if any", example=None)

# Single address check
class TxCheckRequest(BaseModel):
    to: AddressStr = Field(..., example="0xAbC1234567890abcdefABC1234567890abcdefAB")

class TxCheckResponse(BaseResponse):
    to: AddressStr = Field(..., description="Recipient address")
    blocked: bool = Field(..., description="Whether the address is blacklisted", example=True)

    class Config:
        schema_extra = {
            "example": {
                "to": "0xAbC1234567890abcdefABC1234567890abcdefAB",
                "blocked": True,
                "message": "Address is blacklisted",
                "status_code": 200,
                "error": None
            }
        }

# Optional: batch address check support
class BatchTxCheckRequest(BaseModel):
    addresses: list[AddressStr] = Field(..., example=[
        "0xAbC1234567890abcdefABC1234567890abcdefAB",
        "0x1111111111111111111111111111111111111111"
    ])

class BatchTxCheckResponseItem(BaseModel):
    to: AddressStr
    blocked: bool

class BatchTxCheckResponse(BaseResponse):
    results: list[BatchTxCheckResponseItem]

    class Config:
        schema_extra = {
            "example": {
                "results": [
                    {"to": "0xAbC1234567890abcdefABC1234567890abcdefAB", "blocked": True},
                    {"to": "0x1111111111111111111111111111111111111111", "blocked": False}
                ],
                "message": "Batch check completed",
                "status_code": 200,
                "error": None
            }
        }
