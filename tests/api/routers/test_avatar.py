import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from google.api_core import exceptions as google_exceptions
from api.main import app
from api.exceptions import ApiKeyError, ImageGenerationError

client = TestClient(app)

@pytest.fixture
def mock_genai_client():
    with patch("api.routers.avatar.genai.Client") as mock:
        yield mock

def test_generate_avatar_success(mock_genai_client):
    # Arrange
    mock_response_iterator = iter([
        MagicMock(candidates=[MagicMock(content=MagicMock(parts=[MagicMock(inline_data=MagicMock(data=b'fakedata'))]))]),
    ])
    mock_genai_client.return_value.models.generate_content_stream.return_value = mock_response_iterator

    request_body = {
        "settings": {
            "app_name": "test_app",
            "agent_description": "A test agent",
            "context_dict": {"context": {"role": "user"}},
            "goal_description": "Test goal",
            "analyse_instruction": "Test instruction",
            "voice_name": "Test voice",
            "language_code": "en-US",
            "gemini_api_key": "fake_key"
        }
    }

    # Act
    response = client.post("/api/avatar/generate", json=request_body)

    # Assert
    assert response.status_code == 200
    assert "image" in response.json()

def test_generate_avatar_api_key_error(mock_genai_client):
    # Arrange
    mock_genai_client.side_effect = google_exceptions.GoogleAPICallError("invalid api key")

    request_body = {
        "settings": {
            "app_name": "test_app",
            "agent_description": "A test agent",
            "context_dict": {"context": {"role": "user"}},
            "goal_description": "Test goal",
            "analyse_instruction": "Test instruction",
            "voice_name": "Test voice",
            "language_code": "en-US",
            "gemini_api_key": "invalid_key"
        }
    }

    # Act
    response = client.post("/api/avatar/generate", json=request_body)

    # Assert
    assert response.status_code == 400
    assert response.json() == {"message": "API key is invalid or missing."}

def test_generate_avatar_image_generation_error(mock_genai_client):
    # Arrange
    mock_genai_client.return_value.models.generate_content_stream.side_effect = Exception("Some other error")

    request_body = {
        "settings": {
            "app_name": "test_app",
            "agent_description": "A test agent",
            "context_dict": {"context": {"role": "user"}},
            "goal_description": "Test goal",
            "analyse_instruction": "Test instruction",
            "voice_name": "Test voice",
            "language_code": "en-US",
            "gemini_api_key": "valid_key"
        }
    }

    # Act
    response = client.post("/api/avatar/generate", json=request_body)

    # Assert
    assert response.status_code == 500
    assert response.json() == {"message": "Failed to generate image."}
