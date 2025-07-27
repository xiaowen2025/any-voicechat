import asyncio
import websockets
import json
import base64
import os
import logging

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
WEBSOCKET_URI = "ws://localhost:8000/ws/123?is_audio=true"
AUDIO_CHUNKS_TO_SEND = 10
CHUNK_INTERVAL_SECONDS = 0.2
# Each chunk is 0.2s of 16kHz 16-bit mono PCM audio
# 16000 samples/sec * 2 bytes/sample * 0.2 sec = 6400 bytes
AUDIO_CHUNK_SIZE_BYTES = 6400
# ---

async def receive_messages(websocket):
    """Listens for messages from the server and prints them."""
    logging.info("[Receiver] Task started, waiting for messages.")
    try:
        async for message in websocket:
            data = json.loads(message)
            if "mime_type" in data:
                if data["mime_type"] == "text/plain":
                    logging.info(f"<-- RECEIVED TEXT: {data['data']}")
                elif data["mime_type"] == "audio/pcm":
                    audio_chunk = base64.b64decode(data['data'])
                    logging.info(f"<-- RECEIVED AUDIO of {len(audio_chunk)} bytes")
            elif "turn_complete" in data:
                logging.info(f"<-- RECEIVED EVENT: Turn Complete={data['turn_complete']}, Interrupted={data['interrupted']}")
            else:
                logging.info(f"<-- RECEIVED UNKNOWN: {data}")
    except websockets.exceptions.ConnectionClosed as e:
        logging.warning(f"[Receiver] Connection closed by server: {e}")
    except Exception as e:
        logging.error(f"[Receiver] An error occurred: {e}", exc_info=True)
    finally:
        logging.info("[Receiver] Task finished.")

async def send_audio(websocket):
    """Sends a chunk of dummy audio data at a regular interval."""
    logging.info("[Sender] Task started.")
    try:
        for i in range(AUDIO_CHUNKS_TO_SEND):
            dummy_pcm_data = os.urandom(AUDIO_CHUNK_SIZE_BYTES)
            base64_data = base64.b64encode(dummy_pcm_data).decode('ascii')
            message = {"mime_type": "audio/pcm", "data": base64_data}
            
            await websocket.send(json.dumps(message))
            logging.info(f"--> Sent audio chunk {i+1}/{AUDIO_CHUNKS_TO_SEND}")
            
            await asyncio.sleep(CHUNK_INTERVAL_SECONDS)
            
    except websockets.exceptions.ConnectionClosed as e:
        logging.error(f"[Sender] Could not send audio, connection closed: {e}")
    except Exception as e:
        logging.error(f"[Sender] An error occurred: {e}", exc_info=True)
    finally:
        logging.info("[Sender] Task finished.")


async def main():
    """Connects to the websocket and runs the send/receive tasks."""
    logging.info(f"Connecting to {WEBSOCKET_URI}...")
    try:
        async with websockets.connect(WEBSOCKET_URI) as websocket:
            logging.info("Connection established!")
            
            receive_task = asyncio.create_task(receive_messages(websocket))
            send_task = asyncio.create_task(send_audio(websocket))
            
            # Wait for either task to complete
            done, pending = await asyncio.wait(
                [receive_task, send_task],
                return_when=asyncio.FIRST_COMPLETED
            )
            
            logging.info("A task has finished. Cleaning up remaining tasks.")
            for task in pending:
                task.cancel()
            
    except ConnectionRefusedError:
        logging.error("Failed to connect. Connection refused.")
        logging.error("Please ensure the main application server is running on localhost:8000.")
    except Exception as e:
        logging.error(f"An unexpected error occurred in main: {e}", exc_info=True)
    finally:
        logging.info("Script finished.")

if __name__ == "__main__":
    # uv run python -m tests.test_websocket_audio
    asyncio.run(main())