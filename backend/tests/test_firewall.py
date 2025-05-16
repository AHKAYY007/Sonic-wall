import pytest
from unittest.mock import patch
from app.firewall.rules import is_address_blocked

# ✅ Valid address that is blocked
@patch("app.firewall.rules.get_firewall_contract")
def test_blacklist_check_true(mock_contract):
    mock_contract.return_value.functions.isBlocked.return_value.call.return_value = True
    address = "0x000000000000000000000000000000000000dead"

    result = is_address_blocked(address)

    assert isinstance(result, bool)
    assert result is True
    mock_contract.return_value.functions.isBlocked.return_value.call.assert_called_once()

# ✅ Valid address that is NOT blocked
@patch("app.firewall.rules.get_firewall_contract")
def test_blacklist_check_false(mock_contract):
    mock_contract.return_value.functions.isBlocked.return_value.call.return_value = False
    address = "0x1111111111111111111111111111111111111111"

    result = is_address_blocked(address)

    assert isinstance(result, bool)
    assert result is False
    mock_contract.return_value.functions.isBlocked.return_value.call.assert_called_once()

# ❌ Empty address should raise ValueError
def test_blacklist_empty_address():
    with pytest.raises(ValueError, match="Invalid Ethereum address."):
        is_address_blocked("")

# ❌ Invalid format address
def test_blacklist_malformed_address():
    with pytest.raises(ValueError, match="Invalid Ethereum address."):
        is_address_blocked("not-an-address")

# 🧨 Blockchain call throws error → should log + return False
@patch("app.firewall.rules.get_firewall_contract")
def test_blacklist_call_error_returns_false(mock_contract):
    mock_contract.return_value.functions.isBlocked.return_value.call.side_effect = Exception("Contract call failed")
    address = "0x2222222222222222222222222222222222222222"

    result = is_address_blocked(address)

    assert result is False
