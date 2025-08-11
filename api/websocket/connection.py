import asyncio
import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from api.settings import DATA_PATH
from api.websocket.agent import start_agent_session
from api.websocket.messaging import agent_to_client_messaging, client_to_agent_messaging

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, is_audio: str):
    """Client websocket endpoint"""
    # Wait for client connection
    print(f"Client #{user_id} connected, audio mode: {is_audio}")
    settings = json.loads(open(f"{DATA_PATH}/settings.json").read())

    await websocket.accept()
    # Start agent session
    user_id_str = str(user_id)
    live_events, live_request_queue = await start_agent_session(
        user_id_str,
        settings=settings,
        is_audio=(is_audio == "true")
    )

    # Start tasks
    agent_to_client_task = asyncio.create_task(
        agent_to_client_messaging(websocket, live_events)
    )
    client_to_agent_task = asyncio.create_task(
        client_to_agent_messaging(websocket, live_request_queue)
    )

    # Wait until the websocket is disconnected or an error occurs
    tasks = [agent_to_client_task, client_to_agent_task]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)

    for task in pending:
        task.cancel()

    for task in done:
        try:
            task.result()
        except WebSocketDisconnect:
            break
        except Exception as e:
            print(f"Task finished with unexpected exception: {e}")


    # Close LiveRequestQueue
    live_request_queue.close()

    # Disconnected
    print(f"Client #{user_id} disconnected")
