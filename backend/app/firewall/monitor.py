import os
import json
import logging
from web3 import Web3
from web3.contract import Contract
from web3.middleware import geth_poa_middleware
from eth_utils import is_address
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional

# Load environment variables
load_dotenv()

SONIC_RPC_URL = os.getenv("SONIC_RPC_URL")
FIREWALL_CONTRACT_ADDRESS = os.getenv("FIREWALL_CONTRACT_ADDRESS")

# Logger setup
logger = logging.getLogger("sonic_integration")
logging.basicConfig(level=logging.INFO)

# Validate environment variables
if not SONIC_RPC_URL:
    raise EnvironmentError("Missing SONIC_RPC_URL in environment variables.")
if not FIREWALL_CONTRACT_ADDRESS:
    raise EnvironmentError("Missing FIREWALL_CONTRACT_ADDRESS in environment variables.")
if not is_address(FIREWALL_CONTRACT_ADDRESS):
    raise ValueError(f"Invalid Ethereum address: {FIREWALL_CONTRACT_ADDRESS}")

# Web3 initialization
w3 = Web3(Web3.HTTPProvider(SONIC_RPC_URL))

# Optional: Add middleware (useful for Sonic if it runs like BSC/POA chains)
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

if not w3.isConnected():
    raise ConnectionError(f"Failed to connect to Sonic RPC at {SONIC_RPC_URL}")
logger.info(f"Connected to Sonic RPC: {SONIC_RPC_URL}")

# Load ABI
ABI_PATH = Path(__file__).resolve().parent.parent / "contracts" / "firewall_abi.json"
if not ABI_PATH.exists():
    raise FileNotFoundError(f"ABI file not found at: {ABI_PATH}")

try:
    with open(ABI_PATH, "r") as abi_file:
        contract_abi = json.load(abi_file)
except json.JSONDecodeError as e:
    raise ValueError(f"Failed to parse ABI JSON: {e}")

# Lazy-loaded singleton contract
_firewall_contract: Optional[Contract] = None

def get_firewall_contract(force_reload: bool = False) -> Contract:
    """
    Returns a singleton instance of the firewall smart contract.
    Set `force_reload=True` to reinitialize the contract instance.
    """
    global _firewall_contract
    if force_reload or _firewall_contract is None:
        logger.debug("Loading firewall contract instance.")
        _firewall_contract = w3.eth.contract(
            address=Web3.to_checksum_address(FIREWALL_CONTRACT_ADDRESS),
            abi=contract_abi
        )
        logger.info("Firewall contract loaded successfully.")
    return _firewall_contract

def get_blacklist_status(address: str) -> bool:
    """
    Wrapper for checking if an address is blacklisted.
    """
    if not is_address(address):
        raise ValueError("Invalid Ethereum address.")
    contract = get_firewall_contract()
    return contract.functions.isBlocked(Web3.to_checksum_address(address)).call()
