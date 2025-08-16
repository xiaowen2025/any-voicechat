import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from google.api_core import exceptions as google_exceptions
from api.main import app

client = TestClient(app)

@pytest.fixture
def mock_genai_client():
    with patch("google.genai.Client") as mock:
        yield mock

def test_verify_api_key_success(mock_genai_client):
    # Arrange
    mock_genai_client.return_value.models.generate_content.return_value = None
    request_body = {"key": "valid_key"}

    # Act
    response = client.post("/api/verify_api_key", json=request_body)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "API Key verified and set."}

def test_verify_api_key_failure(mock_genai_client):
    # Arrange
    mock_genai_client.return_value.models.generate_content.side_effect = google_exceptions.GoogleAPICallError("Invalid API Key")
    request_body = {"key": "invalid_key"}

    # Act
    response = client.post("/api/verify_api_key", json=request_body)

    # Assert
    assert response.status_code == 200
    assert response.json()["status"] == "error"
    assert "Invalid API Key" in response.json()["message"]


def test_set_api_key():
    # Arrange
    request_body = {"key": "any_key"}

    # Act
    response = client.post("/api/set_api_key", json=request_body)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "API Key set."}
