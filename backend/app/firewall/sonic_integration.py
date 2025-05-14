import os
import json
import logging
from web3 import Web3
from eth_utils import is_address
from pathlib import Path
from dotenv import load_dotenv
import sentry_sdk

load_dotenv()

logger = logging.getLogger("firewall.sonic")

# Load and validate environment variables
SONIC_RPC_URL = os.getenv("SONIC_RPC_URL")
FIREWALL_CONTRACT_ADDRESS = os.getenv("FIREWALL_CONTRACT_ADDRESS")

if not SONIC_RPC_URL:
    logger.critical("Missing SONIC_RPC_URL in environment")
    raise EnvironmentError("Missing SONIC_RPC_URL in .env")

if not FIREWALL_CONTRACT_ADDRESS:
    logger.critical("Missing FIREWALL_CONTRACT_ADDRESS in environment")
    raise EnvironmentError("Missing FIREWALL_CONTRACT_ADDRESS in .env")

if not is_address(FIREWALL_CONTRACT_ADDRESS):
    logger.critical("Invalid Ethereum address format for FIREWALL_CONTRACT_ADDRESS")
    raise ValueError("FIREWALL_CONTRACT_ADDRESS is not a valid Ethereum address")

# Connect to the Sonic RPC
try:
    w3 = Web3(Web3.HTTPProvider(SONIC_RPC_URL))
    if not w3.isConnected():
        raise ConnectionError("Web3 failed to connect to Sonic RPC")
    logger.info("Successfully connected to Sonic RPC.")
except Exception as e:
    logger.critical(f"Web3 connection error: {e}", exc_info=True)
    sentry_sdk.capture_exception(e)
    raise ConnectionError(f"Failed to connect to Sonic RPC at {SONIC_RPC_URL}")

# Load contract ABI
ABI_PATH = Path(__file__).resolve().parent.parent / "contracts" / "firewall_abi.json"
if not ABI_PATH.exists():
    logger.critical(f"ABI file not found at: {ABI_PATH}")
    raise FileNotFoundError(f"Firewall contract ABI file missing at {ABI_PATH}")

try:
    with ABI_PATH.open("r") as f:
        contract_abi = json.load(f)
except Exception as e:
    logger.error("Failed to load contract ABI", exc_info=True)
    sentry_sdk.capture_exception(e)
    raise ValueError("Could not parse the contract ABI")

# Lazy singleton contract pattern
_firewall_contract = None

def get_firewall_contract():
    """
    Returns the Sonic Firewall contract instance.
    Uses lazy-loading to ensure only one instance is created.
    """
    global _firewall_contract
    if _firewall_contract is None:
        try:
            _firewall_contract = w3.eth.contract(
                address=Web3.to_checksum_address(FIREWALL_CONTRACT_ADDRESS),
                abi=contract_abi
            )
            logger.info("Firewall contract instance initialized")
        except Exception as e:
            logger.error("Failed to instantiate firewall contract", exc_info=True)
            sentry_sdk.capture_exception(e)
            raise RuntimeError("Could not create firewall contract instance")
    return _firewall_contract
