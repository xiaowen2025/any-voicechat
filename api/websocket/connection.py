import asyncio
import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from api.websocket.session import start_agent_session
from api.websocket.messaging import (
    agent_to_client_messaging,
    client_to_agent_messaging,
    SettingsMessage,
)

router = APIRouter()
logger = logging.getLogger(__name__)

async def _setup_agent_session(user_id: str, settings: dict, websocket: WebSocket, is_audio: bool):
    """Sets up the agent session."""
    logger.info("Starting agent session for user %s", user_id)
    return await start_agent_session(
        user_id,
        settings=settings,
        websocket=websocket,
        is_audio=is_audio,
    )

async def _handle_communication(websocket: WebSocket, live_events, live_request_queue):
    """Handles the communication between the client and the agent."""
    agent_to_client_task = asyncio.create_task(
        agent_to_client_messaging(websocket, live_events)
    )
    client_to_agent_task = asyncio.create_task(
        client_to_agent_messaging(websocket, live_request_queue)
    )

    done, pending = await asyncio.wait(
        [agent_to_client_task, client_to_agent_task],
        return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()
    for task in done:
        try:
            task.result()
        except WebSocketDisconnect:
            logger.info("Client disconnected.")
            break
        except Exception as e:
            logger.error(f"Task finished with unexpected exception: {e}", exc_info=True)

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, is_audio: str):
    """Client websocket endpoint"""
    await websocket.accept()
    logger.info(f"Client #{user_id} connected, audio mode: {is_audio}")

    try:
        settings_json = await websocket.receive_text()
        settings_message = SettingsMessage(**json.loads(settings_json))
        logger.info("Received settings from client")

        live_events, live_request_queue = await _setup_agent_session(
            str(user_id),
            settings=settings_message.settings.model_dump(),
            websocket=websocket,
            is_audio=(is_audio == "true"),
        )

        await _handle_communication(websocket, live_events, live_request_queue)

    except WebSocketDisconnect:
        logger.info(f"Client #{user_id} disconnected")
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
    finally:
        logger.info(f"Closing connection for client #{user_id}")
        if 'live_request_queue' in locals() and live_request_queue:
            live_request_queue.close()
