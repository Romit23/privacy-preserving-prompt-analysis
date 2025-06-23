import pytest
from app.privacy_accountant import PrivacyAccountant

@pytest.fixture(scope="function")
def fresh_accountant():
    """Provide a fresh privacy accountant for each test"""
    return PrivacyAccountant(global_budget=10.0)

@pytest.fixture(scope="module")
def test_client():
    from fastapi.testclient import TestClient
    from app.main import app
    
    with TestClient(app) as client:
        yield client