import logging
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

@FIREWALL_CHECK_TIME.time()
def is_address_blocked(to_address: str) -> bool:
    """
    Check if an Ethereum address is blacklisted in the Sonic Firewall contract.
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
