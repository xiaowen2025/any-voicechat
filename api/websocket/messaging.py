import base64
import json
import logging
from typing import Any, Dict
from google.genai.types import Part, Content, Blob
from pydantic import BaseModel, Field, ValidationError
from api.settings import AppSettings

logger = logging.getLogger(__name__)

# Message Models
class SettingsMessage(BaseModel):
    type: str = Field(default="settings", frozen=True)
    settings: AppSettings

class TextMessage(BaseModel):
    type: str = Field(default="text", frozen=True)
    mime_type: str = "text/plain"
    data: str

class AudioMessage(BaseModel):
    type: str = Field(default="audio", frozen=True)
    mime_type: str = "audio/pcm"
    data: str

class AgentTextMessage(BaseModel):
    output_transcription: Dict[str, str]

class AgentAudioMessage(BaseModel):
    mime_type: str = "audio/pcm"
    data: str

class AgentTurnCompleteMessage(BaseModel):
    turn_complete: bool
    interrupted: bool

class AgentInputTranscriptionMessage(BaseModel):
    input_transcription: Dict[str, str]

class UpdateContextMessage(BaseModel):
    type: str = Field(default="context_updated", frozen=True)
    context_dict: Dict[str, Any]

# Agent to Client Messaging Helpers
async def handle_turn_complete(websocket, event):
    if event.turn_complete or event.interrupted:
        message = AgentTurnCompleteMessage(
            turn_complete=event.turn_complete is True,
            interrupted=event.interrupted is True,
        )
        await websocket.send_json(message.model_dump())
        return True
    return False

async def handle_audio_part(websocket, part):
    is_audio = part.inline_data and part.inline_data.mime_type.startswith("audio/pcm")
    if is_audio:
        audio_data = part.inline_data.data
        if audio_data:
            message = AgentAudioMessage(data=base64.b64encode(audio_data).decode("ascii"))
            await websocket.send_json(message.model_dump())
        return True
    return False

async def handle_transcription(websocket, event, part):
    if event.content.role == "user" and part.text:
        message = AgentInputTranscriptionMessage(input_transcription={"text": part.text})
        await websocket.send_json(message.model_dump())
    elif event.content.role == "model" and part.text and event.partial:
        message = AgentTextMessage(output_transcription={"text": part.text})
        await websocket.send_json(message.model_dump())

async def agent_to_client_messaging(websocket, live_events):
    """Agent to client communication"""
    async for event in live_events:
        if await handle_turn_complete(websocket, event):
            continue
        part: Part = event.content and event.content.parts and event.content.parts[0]
        if not part:
            continue
        if await handle_audio_part(websocket, part):
            continue
        await handle_transcription(websocket, event, part)

# Client to Agent Messaging Helpers
def handle_text_message(message_data, live_request_queue):
    message = TextMessage(**message_data)
    content = Content(role="user", parts=[Part.from_text(text=message.data)])
    live_request_queue.send_content(content=content)

def handle_audio_message(message_data, live_request_queue):
    message = AudioMessage(**message_data)
    decoded_data = base64.b64decode(message.data)
    live_request_queue.send_realtime(Blob(data=decoded_data, mime_type=message.mime_type))

async def client_to_agent_messaging(websocket, live_request_queue):
    """Client to agent communication"""
    while True:
        message_json = await websocket.receive_text()
        try:
            message_data = json.loads(message_json)
            message_type = message_data.get("type")

            if message_type == "text":
                handle_text_message(message_data, live_request_queue)
            elif message_type == "audio":
                handle_audio_message(message_data, live_request_queue)
            elif message_type != "settings":
                logger.warning(f"Unsupported message type: {message_type}")
        except (ValidationError, json.JSONDecodeError) as e:
            logger.error(f"Error processing message: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}", exc_info=True)