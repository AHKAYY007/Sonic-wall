import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

# Sample addresses
valid_address_1 = "0x000000000000000000000000000000000000dead"
valid_address_2 = "0x1111111111111111111111111111111111111111"
invalid_address = "not-a-valid-address"
bad_payload = {"addresses": "not-a-list"}

# ----------------------
# ✅ Firewall POST /check
# ----------------------

@patch("app.firewall.rules.get_firewall_contract")
def test_check_tx_success(mock_contract):
    mock_contract.return_value.functions.isBlocked.return_value.call.return_value = True
    response = client.post("/api/check", json={"to": valid_address_1})
    assert response.status_code == 200
    assert response.json() == {
        "to": valid_address_1.lower(),
        "blocked": True,
        "message": "Address is blacklisted"
    }

@patch("app.firewall.rules.get_firewall_contract")
def test_batch_check_tx_success(mock_contract):
    mock_contract.return_value.functions.isBlocked.return_value.call.side_effect = [True, False]
    response = client.post("/api/check/batch", json={"addresses": [valid_address_1, valid_address_2]})
    assert response.status_code == 200
    assert response.json()["results"] == [
        {"to": valid_address_1.lower(), "blocked": True},
        {"to": valid_address_2.lower(), "blocked": False}
    ]

def test_check_tx_invalid_address():
    response = client.post("/api/check", json={"to": invalid_address})
    assert response.status_code == 422

def test_check_tx_missing_to():
    response = client.post("/api/check", json={})
    assert response.status_code == 422

def test_batch_check_invalid_payload():
    response = client.post("/api/check/batch", json=bad_payload)
    assert response.status_code == 422

def test_batch_check_contains_invalid_address():
    response = client.post("/api/check/batch", json={"addresses": [valid_address_1, "bad-address"]})
    assert response.status_code == 422

@patch("app.firewall.rules.get_firewall_contract")
def test_smoke_check(mock_contract):
    mock_contract.return_value.functions.isBlocked.return_value.call.return_value = False
    response = client.post("/api/check", json={"to": valid_address_2})
    assert response.status_code == 200
    assert response.json()["blocked"] is False

# ----------------------
# ✅ Firewall GET /firewall-check/{wallet_address}
# ----------------------

@patch("app.firewall.rules.get_firewall_contract")
def test_firewall_check_valid(mock_contract):
    mock_contract.return_value.functions.isBlocked.return_value.call.return_value = True
    response = client.get(f"/api/firewall-check/{valid_address_1}")
    assert response.status_code == 200
    assert response.json()["blocked"] is True

def test_firewall_check_invalid():
    response = client.get("/api/firewall-check/invalid-address")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid address"

# ----------------------
# ✅ Risk Score GET /risk-score/{wallet_address}
# ----------------------

@patch("app.api.routes.httpx.AsyncClient.get")
@pytest.mark.asyncio
async def test_risk_score_low(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "status": "1",
        "result": [
            {"from": valid_address_1, "to": valid_address_2},
            {"from": valid_address_1, "to": valid_address_2},
            {"from": valid_address_2, "to": valid_address_1}
        ]
    }

    from app.main import app
    from httpx import AsyncClient

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/api/risk-score/{valid_address_1}")
        assert response.status_code == 200
        assert response.json()["risk"] == "low"

@patch("app.api.routes.httpx.AsyncClient.get")
@pytest.mark.asyncio
async def test_risk_score_high(mock_get):
    # High outbound, low inbound
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "status": "1",
        "result": [{"from": valid_address_1, "to": valid_address_2}] * 60
    }

    from app.main import app
    from httpx import AsyncClient

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/api/risk-score/{valid_address_1}")
        assert response.status_code == 200
        assert response.json()["risk"] == "high"

@patch("app.api.routes.httpx.AsyncClient.get")
@pytest.mark.asyncio
async def test_risk_score_empty_wallet(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "status": "0",
        "result": []
    }

    from app.main import app
    from httpx import AsyncClient

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/api/risk-score/{valid_address_2}")
        assert response.status_code == 200
        assert response.json()["risk"] == "high"
