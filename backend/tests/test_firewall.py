import pytest
from unittest.mock import patch
from app.firewall.rules import is_address_blocked

@patch("app.firewall.rules.get_firewall_contract")
def test_blacklist_check(mock_contract):
    # Mock contract's isBlocked() call to return True
    mock_contract.return_value.functions.isBlocked.return_value.call.return_value = True

    address = "0x000000000000000000000000000000000000dead"
    result = is_address_blocked(address)

    assert isinstance(result, bool)
    assert result is True
    assert mock_contract.return_value.functions.isBlocked.return_value.call.called

@patch("app.firewall.rules.get_firewall_contract")
def test_blacklist_check_false(mock_contract):
    mock_contract.return_value.functions.isBlocked.return_value.call.return_value = False
    address = "0x1111111111111111111111111111111111111111"
    assert is_address_blocked(address) is False



@patch("app.firewall.rules.get_firewall_contract")
def test_blacklist_empty_address(mock_contract):
    with pytest.raises(ValueError):
        is_address_blocked("")
