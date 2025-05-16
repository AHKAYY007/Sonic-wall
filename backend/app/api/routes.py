from fastapi import APIRouter, HTTPException, Request
from app.api.schemas import (
    TxCheckRequest,
    TxCheckResponse,
    BatchTxCheckRequest,
    BatchTxCheckResponse,
    BatchTxCheckResponseItem,
)
from app.firewall.rules import is_address_blocked, get_risk_score
import logging
from opentelemetry import trace

router = APIRouter()
logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


@router.post(
    "/check",
    response_model=TxCheckResponse,
    tags=["Firewall"],
    summary="Check if address is blacklisted",
    description="Checks if a specific wallet address is blocked by the Sonic firewall smart contract."
)
async def check_tx(payload: TxCheckRequest, request: Request):
    with tracer.start_as_current_span("check_single_tx"):
        try:
            blocked = is_address_blocked(payload.to)
            logger.info(
                "Checked address",
                extra={
                    "address": payload.to,
                    "blocked": blocked,
                    "client": request.client.host,
                    "path": request.url.path
                }
            )
            return TxCheckResponse(
                to=payload.to,
                blocked=blocked,
                message="Address is blacklisted" if blocked else "Address is not blacklisted",
                status_code=200,
                error=None
            )
        except Exception as e:
            logger.exception("Blockchain interaction failed")
            raise HTTPException(status_code=502, detail="Blockchain interaction failed")


@router.post(
    "/check/batch",
    response_model=BatchTxCheckResponse,
    tags=["Firewall"],
    summary="Batch check of blacklisted addresses",
    description="Checks a list of wallet addresses to determine if they are blocked by the Sonic firewall smart contract."
)
async def batch_check(payload: BatchTxCheckRequest, request: Request):
    with tracer.start_as_current_span("check_batch_tx"):
        results = []
        try:
            for address in payload.addresses:
                blocked = is_address_blocked(address)
                logger.info(
                    "Batch check result",
                    extra={
                        "address": address,
                        "blocked": blocked,
                        "client": request.client.host,
                        "path": request.url.path
                    }
                )
                results.append(BatchTxCheckResponseItem(to=address, blocked=blocked))

            return BatchTxCheckResponse(
                results=results,
                message="Batch check completed",
                status_code=200,
                error=None
            )
        except Exception as e:
            logger.exception("Batch blockchain interaction failed")
            raise HTTPException(status_code=502, detail="Batch blockchain interaction failed")


@router.get("/risk-score/{wallet_address}", tags=["Firewall"])
async def risk_score(wallet_address: str):
    return await get_risk_score(wallet_address)


@router.get("/firewall-check/{wallet_address}", tags=["Firewall"])
def firewall_check(wallet_address: str):
    try:
        return {"blocked": is_address_blocked(wallet_address)}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid address")
