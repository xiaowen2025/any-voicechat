import os
import json
from fastapi import APIRouter
from api.settings import APP_EXAMPLES_PATH

router = APIRouter()


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
