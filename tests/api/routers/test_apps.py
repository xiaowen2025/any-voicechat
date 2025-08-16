import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

@pytest.fixture
def mock_app_service():
    with patch("api.services.app_service.get_app_settings") as mock_get_settings, \
         patch("api.services.app_service.get_apps") as mock_get_apps:
        yield mock_get_settings, mock_get_apps

def test_get_app_settings(mock_app_service):
    # Arrange
    mock_get_settings, _ = mock_app_service
    mock_get_settings.return_value = {"setting1": "value1"}
    app_id = "test_app"

    # Act
    response = client.get(f"/api/apps/{app_id}/settings")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"setting1": "value1"}
    mock_get_settings.assert_called_once_with(app_id)

def test_get_apps(mock_app_service):
    # Arrange
    _, mock_get_apps = mock_app_service
    mock_get_apps.return_value = [{"id": "app1"}, {"id": "app2"}]

    # Act
    response = client.get("/api/apps")

    # Assert
    assert response.status_code == 200
    assert response.json() == [{"id": "app1"}, {"id": "app2"}]
    mock_get_apps.assert_called_once()
