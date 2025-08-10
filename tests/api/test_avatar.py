import pytest
import base64
from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient
from api.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_generate_avatar(client):
    with patch('google.generativeai.Client') as mock_client:
        # Mock the client and its methods
        mock_gen_image_response = MagicMock()
        mock_gen_image_response.generated_images = [MagicMock()]
        mock_gen_image_response.generated_images[0].image.image_bytes = b'test_image_bytes'

        mock_instance = mock_client.return_value
        mock_instance.models.generate_images.return_value = mock_gen_image_response

        # Call the endpoint
        response = client.post("/api/avatar/generate", json={"prompt": "a test prompt"})

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert "image" in data
        assert data["image"] == base64.b64encode(b'test_image_bytes').decode('utf-8')

        # Verify that the mock was called
        mock_instance.models.generate_images.assert_called_once()
