import os
import json
from fastapi import APIRouter
from api.settings import APP_EXAMPLES_PATH
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import json
import os

from api.settings import APP_EXAMPLES_PATH

router = APIRouter()


@router.get("/api/apps/{app_id}/settings")
async def get_app_settings(app_id: str):
    """
    Retrieves the settings for a specific app.
    """
    try:
        filepath = os.path.join(APP_EXAMPLES_PATH, f"{app_id}.json")
        if not os.path.exists(filepath):
            return JSONResponse(content={"error": "App not found"}, status_code=404)
        with open(filepath, "r") as f:
            settings = json.load(f)
        return JSONResponse(content=settings)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.get("/api/apps")
async def get_apps():
    """
    Reads all app example JSON files, extracts key information,
    and returns a list of app configurations.
    """
    apps = []
    app_files = [f for f in os.listdir(APP_EXAMPLES_PATH) if f.endswith(".json")]

    for i, filename in enumerate(app_files):
        filepath = os.path.join(APP_EXAMPLES_PATH, filename)
        with open(filepath, "r") as f:
            data = json.load(f)
            apps.append({
                "id": filename.replace(".json", ""),
                "name": data.get("app_name", "Unnamed App"),
                "summary": data.get("agent_description", "No summary available.")
            })
    return apps
