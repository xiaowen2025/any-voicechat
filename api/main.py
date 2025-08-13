import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from api import api_key, analyse, avatar, apps
from api.websocket import connection as websocket
from api.exceptions import (
    ApiKeyError,
    ImageGenerationError,
    AppNotFoundError,
    MalformedAppConfigError,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

# Exception handlers
@app.exception_handler(ApiKeyError)
async def api_key_error_handler(request: Request, exc: ApiKeyError):
    logger.error(f"ApiKeyError: {exc}")
    return JSONResponse(
        status_code=400,
        content={"message": "API key is invalid or missing."},
    )

@app.exception_handler(ImageGenerationError)
async def image_generation_error_handler(request: Request, exc: ImageGenerationError):
    logger.error(f"ImageGenerationError: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Failed to generate image."},
    )

@app.exception_handler(AppNotFoundError)
async def app_not_found_error_handler(request: Request, exc: AppNotFoundError):
    logger.error(f"AppNotFoundError: {exc}")
    return JSONResponse(
        status_code=404,
        content={"message": str(exc)},
    )

@app.exception_handler(MalformedAppConfigError)
async def malformed_app_config_error_handler(request: Request, exc: MalformedAppConfigError):
    logger.error(f"MalformedAppConfigError: {exc}")
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )

app.include_router(analyse.router)
app.include_router(api_key.router)
app.include_router(websocket.router)
app.include_router(avatar.router)
app.include_router(apps.router)

app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")


def main():
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
