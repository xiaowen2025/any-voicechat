import json
from google.genai.types import (
    SpeechConfig,
    VoiceConfig,
    PrebuiltVoiceConfig,
)
from google.adk.runners import InMemoryRunner
from google.adk.agents import LiveRequestQueue
from google.adk.agents.run_config import RunConfig
from google.adk.tools import google_search


from api.voice_agent import create_agent
from api.websocket.messaging import UpdateContextMessage


async def start_agent_session(user_id, settings, websocket, is_audio=False):
    async def edit_context_dict(context_dict: dict) -> dict:
        """Updates the context dictionary and informs the client via WebSocket.

        Args:
            context_dict (dict): The new context dictionary.
        """
        update_context_message = UpdateContextMessage(context_dict=context_dict)
        await websocket.send_json(update_context_message.model_dump())
        return {"status": "Context updated successfully."}

    tools = [edit_context_dict]
    if settings.get("search_tool"):
        tools.append(google_search)

    # Create a Runner
    runner = InMemoryRunner(
        app_name=settings["app_name"],
        agent=create_agent(
            settings,
            tools=tools
        ),
    )

    # Create a Session
    session = await runner.session_service.create_session(
        app_name=settings["app_name"],
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
    run_config = RunConfig(
        response_modalities=[modality],
        speech_config=speech_config,
        input_audio_transcription={},
        output_audio_transcription={},
    )

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
