import asyncio
import base64
import json
import os
from google.genai.types import (
    Part,
    Content,
    Blob,
    SpeechConfig,
    VoiceConfig,
    PrebuiltVoiceConfig,
)

from google.adk.runners import InMemoryRunner
from google.adk.agents import LiveRequestQueue
from google.adk.agents.run_config import RunConfig

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

from api.voice_agent import create_agent
from api.settings import DATA_PATH


async def start_agent_session(user_id, settings, is_audio=False):
    app_name = settings["app_name"]
    # Create a Runner
    runner = InMemoryRunner(
        app_name=app_name,
        agent=create_agent(settings),
    )

    # Create a Session
    session = await runner.session_service.create_session(
        app_name=app_name,
        user_id=user_id,  # Replace with actual user ID
    )

    # Set response modality
    modality = "AUDIO" if is_audio else "TEXT"
    speech_config = SpeechConfig(
        language_code=settings["language_code"],
        voice_config=VoiceConfig(
            prebuilt_voice_config=PrebuiltVoiceConfig(
                voice_name=settings["voice_name"]
            )
        ),
    )
    run_config = RunConfig(response_modalities=[modality], speech_config=speech_config)

    # Create a LiveRequestQueue for this session
    live_request_queue = LiveRequestQueue()

    # Start agent session
    live_events = runner.run_live(
        user_id=user_id,
        session_id=session.id,
        live_request_queue=live_request_queue,
        run_config=run_config,
    )
    return live_events, live_request_queue
