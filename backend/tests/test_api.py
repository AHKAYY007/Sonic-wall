import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

# 🔁 Sample addresses
valid_address_1 = "0x000000000000000000000000000000000000dead"
valid_address_2 = "0x1111111111111111111111111111111111111111"
invalid_address = "not-a-valid-address"
bad_payload = {"addresses": "not-a-list"}

# ✅ Unit: Single valid check
@patch("app.firewall.rules.get_firewall_contract")
def test_check_tx_success(mock_contract):
    mock_contract.return_value.functions.isBlocked.return_value.call.return_value = True

    response = client.post("/api/check", json={"to": valid_address_1})
    assert response.status_code == 200
    data = response.json()

    assert data == {
        "to": valid_address_1.lower(),
        "blocked": True,
        "message": "Address is blacklisted"
    }


# ✅ Unit: Batch check (mixed results)
@patch("app.firewall.rules.get_firewall_contract")
def test_batch_check_tx_success(mock_contract):
    mock_contract.return_value.functions.isBlocked.return_value.call.side_effect = [True, False]

    response = client.post("/api/check/batch", json={"addresses": [valid_address_1, valid_address_2]})
    assert response.status_code == 200

    results = response.json()["results"]
    assert results == [
        {"to": valid_address_1.lower(), "blocked": True},
        {"to": valid_address_2.lower(), "blocked": False}
    ]


# ❌ Invalid: Non-EVM address format
def test_check_tx_invalid_address():
    response = client.post("/api/check", json={"to": invalid_address})
    assert response.status_code == 422  # FastAPI validation error


# ❌ Invalid: Missing required 'to'
def test_check_tx_missing_to():
    response = client.post("/api/check", json={})
    assert response.status_code == 422


# ❌ Invalid: Batch payload not a list
def test_batch_check_invalid_payload():
    response = client.post("/api/check/batch", json=bad_payload)
    assert response.status_code == 422


# ❌ Invalid: Batch contains malformed address
def test_batch_check_contains_invalid_address():
    response = client.post("/api/check/batch", json={"addresses": [valid_address_1, "bad-address"]})
    assert response.status_code == 422


# ✅ Smoke test: actual running server
@patch("app.firewall.rules.get_firewall_contract")
def test_smoke_check(mock_contract):
    mock_contract.return_value.functions.isBlocked.return_value.call.return_value = False
    response = client.post("/api/check", json={"to": valid_address_2})
    assert response.status_code == 200
    assert response.json()["blocked"] is False
