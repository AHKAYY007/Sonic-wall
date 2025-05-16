import logging
import os
from web3 import Web3
from eth_utils import is_address
from app.firewall.sonic_integration import get_firewall_contract
from prometheus_client import Counter, Summary
import sentry_sdk

logger = logging.getLogger("firewall.rules")

# Prometheus metrics
FIREWALL_CALLS = Counter("firewall_calls_total", "Total firewall address checks")
FIREWALL_ERRORS = Counter("firewall_errors_total", "Firewall errors during address checks")
FIREWALL_CHECK_TIME = Summary("firewall_check_duration_seconds", "Time taken for firewall contract call")

# Sonic Blaze RPC setup
RPC_URL = os.getenv("SONIC_RPC_URL", "https://rpc.blaze.soniclabs.com")
w3 = Web3(Web3.HTTPProvider(RPC_URL))


@FIREWALL_CHECK_TIME.time()
def is_address_blocked(to_address: str) -> bool:
    """
    On-chain firewall check using Sonic Firewall contract.
    """
    if not is_address(to_address):
        logger.warning(f"[Firewall] Invalid Ethereum address: {to_address}")
        raise ValueError("Invalid Ethereum address.")

    FIREWALL_CALLS.inc()

    try:
        contract = get_firewall_contract()
        checksum_address = Web3.to_checksum_address(to_address)
        blocked = contract.functions.isBlocked(checksum_address).call()
        logger.info(f"[Firewall] {checksum_address} → Blocked: {blocked}")
        return blocked

    except Exception as e:
        FIREWALL_ERRORS.inc()
        logger.error(f"[Firewall] Contract call failed: {e}", exc_info=True)
        sentry_sdk.capture_exception(e)
        return False


async def get_risk_score(wallet_address: str) -> dict:
    """
    Risk scoring using Sonic Blaze RPC (no Etherscan).
    """
    if not is_address(wallet_address):
        return {"risk": "high", "reason": "Invalid wallet address"}

    try:
        checksum_address = Web3.to_checksum_address(wallet_address)
        tx_count = w3.eth.get_transaction_count(checksum_address)

        if tx_count == 0:
            return {"risk": "high", "reason": "Empty wallet"}
        elif tx_count < 3:
            return {"risk": "medium", "reason": "New or low-activity wallet"}
        else:
            return {"risk": "low", "reason": "Transaction activity looks normal"}

    except Exception as e:
        logger.error(f"[RiskScore] RPC error: {e}")
        sentry_sdk.capture_exception(e)
        return {"risk": "unknown", "reason": "Failed to fetch tx count"}
