from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List, Dict, Any

from api.services import app_service

router = APIRouter()

@router.get("/api/apps/{app_id}/settings")
async def get_app_settings(app_id: str) -> JSONResponse:
    """
    Retrieves the settings for a specific app.
    """
    settings = app_service.get_app_settings(app_id)
    return JSONResponse(content=settings)

@router.get("/api/apps")
async def get_apps() -> List[Dict[str, Any]]:
    """
    Reads all app example JSON files, extracts key information,
    and returns a list of app configurations.
    """
    return app_service.get_apps()
