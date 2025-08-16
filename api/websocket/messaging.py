import asyncio
import base64
import json
import logging
from typing import Any, Dict
from google.genai.types import (
    Part,
    Content,
    Blob,
)
from pydantic import BaseModel, Field, ValidationError
from api.settings import AppSettings

logger = logging.getLogger(__name__)

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


async def agent_to_client_messaging(websocket, live_events):
    """Agent to client communication"""
    while True:
        async for event in live_events:

            # If the turn complete or interrupted, send it
            if event.turn_complete or event.interrupted:
                message = AgentTurnCompleteMessage(
                    turn_complete=event.turn_complete is True,
                    interrupted=event.interrupted is True,
                )
                await websocket.send_json(message.model_dump())
                continue

            # Read the Content and its first Part
            part: Part = (
                event.content and event.content.parts and event.content.parts[0]
            )
            if not part:
                continue

            # If it's audio, send Base64 encoded audio data
            is_audio = part.inline_data and part.inline_data.mime_type.startswith("audio/pcm")
            if is_audio:
                audio_data = part.inline_data and part.inline_data.data
                if audio_data:
                    message = AgentAudioMessage(
                        data=base64.b64encode(audio_data).decode("ascii")
                    )
                    await websocket.send_json(message.model_dump())
                    continue
            # User message transcription
            if event.content.role == "user" and part.text:
                message = AgentInputTranscriptionMessage(
                    input_transcription={"text": part.text}
                )
                await websocket.send_json(message.model_dump())

            # Agent message transcription
            elif event.content.role == "model" and part.text and event.partial:
                message = AgentTextMessage(
                    output_transcription={"text": part.text}
                )
                await websocket.send_json(message.model_dump())


async def client_to_agent_messaging(websocket, live_request_queue):
    """Client to agent communication"""
    while True:
        message_json = await websocket.receive_text()
        try:
            message_data = json.loads(message_json)
            message_type = message_data.get("type")

            if message_type == "text":
                message = TextMessage(**message_data)
                content = Content(role="user", parts=[Part.from_text(text=message.data)])
                live_request_queue.send_content(content=content)
            elif message_type == "audio":
                message = AudioMessage(**message_data)
                decoded_data = base64.b64decode(message.data)
                live_request_queue.send_realtime(Blob(data=decoded_data, mime_type=message.mime_type))
            # The settings message is handled in the connection setup, so we ignore it here.
            elif message_type == "settings":
                pass
            else:
                logger.warning(f"Unsupported message type: {message_type}")

        except (ValidationError, json.JSONDecodeError) as e:
            logger.error(f"Error processing message: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}", exc_info=True)