from pydantic import ConstrainedStr
from eth_utils import is_address

class AddressStr(ConstrainedStr):
    """Custom Pydantic string type for Ethereum addresses."""
    @classmethod
    def validate(cls, value):
        if not is_address(value):
            raise ValueError("Invalid Ethereum address format")
        return value
