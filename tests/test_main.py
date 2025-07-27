import pytest
import asyncio
import json
import base64
from unittest.mock import patch, MagicMock, AsyncMock

from fastapi.testclient import TestClient
from google.genai.types import Part, Content, Blob

from api.main import app, agent_to_client_messaging, client_to_agent_messaging


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.asyncio
async def test_root_endpoint(client):
    with patch("fastapi.responses.FileResponse") as mock_file_response:
        mock_file_response.return_value = "<html></html>"
        response = client.get("/")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_agent_to_client_messaging():
    """Tests the agent-to-client messaging coroutine."""
    websocket = AsyncMock()
    
    async def mock_events():
        # 1. Yield a text message
        yield MagicMock(
            turn_complete=False,
            interrupted=False,
            content=Content(parts=[Part(text="Hello")]),
            partial=True
        )
        # 2. Yield an audio message
        audio_data = b"some_audio_bytes"
        yield MagicMock(
            turn_complete=False,
            interrupted=False,
            content=Content(parts=[Part(inline_data=Blob(mime_type="audio/pcm", data=audio_data))]),
            partial=False
        )
        # 3. Yield a turn complete event
        yield MagicMock(turn_complete=True, interrupted=False, content=None)

    live_events = mock_events()

    # Run the coroutine and wait for it to complete
    await agent_to_client_messaging(websocket, live_events)

    # Verify calls
    assert websocket.send_text.call_count == 3
    
    # Check text message
    websocket.send_text.assert_any_call(json.dumps({
        "mime_type": "text/plain",
        "data": "Hello"
    }))
    
    # Check audio message
    websocket.send_text.assert_any_call(json.dumps({
        "mime_type": "audio/pcm",
        "data": base64.b64encode(audio_data).decode("ascii")
    }))

    # Check turn complete message
    websocket.send_text.assert_any_call(json.dumps({
        "turn_complete": True,
        "interrupted": False
    }))


@pytest.mark.asyncio
async def test_client_to_agent_messaging():
    """Tests the client-to-agent messaging coroutine."""
    websocket = AsyncMock()
    live_request_queue = MagicMock()
    live_request_queue.send_content = MagicMock()
    live_request_queue.send_realtime = MagicMock()

    # Mock received messages
    text_message = json.dumps({"mime_type": "text/plain", "data": "Hello Agent"})
    audio_data = b"some_audio_bytes"
    audio_message = json.dumps({
        "mime_type": "audio/pcm",
        "data": base64.b64encode(audio_data).decode("ascii")
    })
    
    # Set up the websocket to return messages in order, then raise an exception to stop
    websocket.receive_text.side_effect = [
        text_message,
        audio_message,
        asyncio.CancelledError  # To break the loop
    ]

    with pytest.raises(asyncio.CancelledError):
        await client_to_agent_messaging(websocket, live_request_queue)

    # Verify calls
    live_request_queue.send_content.assert_called_once()
    live_request_queue.send_realtime.assert_called_once()

    # Check text message content
    sent_content = live_request_queue.send_content.call_args[1]['content']
    assert sent_content.parts[0].text == "Hello Agent"

    # Check audio message content
    sent_blob = live_request_queue.send_realtime.call_args[0][0]
    assert sent_blob.data == audio_data
    assert sent_blob.mime_type == "audio/pcm"
