import pytest
import base64
from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient
from api.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_generate_avatar(client):
    with patch("api.avatar.genai.Client") as mock_client:
        # Mock the client and its methods
        mock_response_iterator = [
            MagicMock(
                candidates=[
                    MagicMock(
                        content=MagicMock(
                            parts=[
                                MagicMock(
                                    inline_data=MagicMock(data=b"test_image_bytes")
                                )
                            ]
                        )
                    )
                ],
                text=None,
            )
        ]

        mock_instance = mock_client.return_value
        mock_instance.models.generate_content_stream.return_value = (
            mock_response_iterator
        )

        test_settings = {
            "app_name": "Test App",
            "agent_description": "a friendly test agent",
            "context_dict": {},
            "goal_description": "testing",
            "notes_taking_instruction": "none",
            "analyse_instruction": "none",
            "voice_name": "echo",
            "language_code": "en-US"
        }

        # Call the endpoint
        response = client.post("/api/avatar/generate", json={"settings": test_settings})

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert "image" in data
        assert data["image"] == base64.b64encode(b"test_image_bytes").decode("utf-8")

        # Verify that the mock was called
        mock_instance.models.generate_content_stream.assert_called_once()
        # Verify the prompt
        args, kwargs = mock_instance.models.generate_content_stream.call_args
        assert "contents" in kwargs
        assert "an avatar for a a friendly test agent" in str(kwargs["contents"])
