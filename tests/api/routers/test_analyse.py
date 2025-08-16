import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

@pytest.fixture
def mock_analysis_service():
    with patch("api.services.analysis_service.analyse_notes") as mock:
        yield mock

def test_post_analyse(mock_analysis_service):
    # Arrange
    mock_analysis_service.return_value = {"summary": "Test summary"}
    request_body = {
        "notes": "These are test notes.",
        "settings": {
            "gemini_api_key": "test_key",
            "context_dict": {"role": "user"},
            "agent_description": "A test agent"
        }
    }

    # Act
    response = client.post("/api/analyse", json=request_body)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Analysis complete", "analysis": {"summary": "Test summary"}}
    mock_analysis_service.assert_called_once()
