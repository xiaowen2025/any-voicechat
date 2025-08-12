from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
import json
import os


from api.settings import APP_EXAMPLES_PATH
from api.dependencies import load_settings

router = APIRouter()


@router.get("/api/settings")
async def get_settings():
    """
    Retrieves the entire settings dictionary.
    """
    try:
        settings = load_settings()
        return JSONResponse(content=settings)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get("/api/context")
async def get_context(settings: dict = Depends(load_settings)):
    """
    Retrieves the context dictionary from the settings.
    """
    context = settings.get("context_dict", {})
    return JSONResponse(content=context)



@router.post("/api/settings/load_app/{app_id}")
async def load_app_settings(app_id: str):
    """
    Loads settings from an app example into the main settings.
    """
    try:
        filepath = os.path.join(APP_EXAMPLES_PATH, f"{app_id}.json")
        if not os.path.exists(filepath):
            return JSONResponse(content={"error": "App not found"}, status_code=404)

        with open(filepath, "r") as f:
            app_settings = json.load(f)

        return JSONResponse(content={"message": f"App '{app_id}' loaded successfully."})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

