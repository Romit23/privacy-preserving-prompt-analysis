import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.privacy_accountant import PrivacyAccountant
from unittest.mock import patch

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def reset_accountant():
    """Reset the privacy accountant before each test"""
    accountant = PrivacyAccountant(global_budget=10.0)
    return accountant

class TestAPIEndpoints:
    """Tests for FastAPI endpoints"""
    
    def test_analyze_endpoint(self, client, reset_accountant):
        response = client.post(
            "/analyze",
            json={"prompt": "My email is test@example.com", "user_id": "test"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "risk_score" in data
        assert data["risk_score"] > 0.7
        assert "privacy_guarantee" in data
    
    def test_analyze_endpoint_no_pii(self, client, reset_accountant):
        response = client.post(
            "/analyze",
            json={"prompt": "Tell me about the weather", "user_id": "test"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["risk_score"] < 0.3
        assert data["needs_review"] is False
    
    @patch('app.database.get_dp_analytics')
    def test_analytics_endpoint(self, mock_analytics, client, reset_accountant):
        mock_analytics.return_value = {
            "top_risks": [{"risk": "PII", "count": 10}],
            "total_analyses": 100,
            "accuracy_95": "±5.00",
            "privacy_guarantee": "ε=0.1"
        }
        
        response = client.get("/analytics")
        assert response.status_code == 200
        data = response.json()
        assert "top_risks" in data
        assert data["epsilon_used"] == 0.1
    
    def test_privacy_budget_endpoint(self, client, reset_accountant):
        response = client.get("/privacy-budget")
        assert response.status_code == 200
        data = response.json()
        assert data["total_budget"] == 10.0
        assert data["used_epsilon"] == 0.0
        assert data["remaining_budget"] == 10.0
    
    def test_budget_exhaustion(self, client, reset_accountant):
        # Exhaust the budget first
        accountant = PrivacyAccountant(global_budget=0.1)
        accountant.allocate_budget(0.1)
        
        with patch('app.main.accountant', accountant):
            response = client.post(
                "/analyze",
                json={"prompt": "test", "user_id": "test"}
            )
            assert response.status_code == 403
            assert "Privacy budget exceeded" in response.json()["detail"]
    
    def test_invalid_input(self, client):
        response = client.post(
            "/analyze",
            json={"wrong_field": "test"}
        )
        assert response.status_code == 422  # FastAPI validation error