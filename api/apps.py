import os
import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from api.settings import APP_EXAMPLES_PATH
from .exceptions import AppNotFoundError, MalformedAppConfigError

router = APIRouter()


@router.get("/api/apps/{app_id}/settings")
async def get_app_settings(app_id: str):
    """
    Retrieves the settings for a specific app.
    """
    filepath = os.path.join(APP_EXAMPLES_PATH, f"{app_id}.json")
    if not os.path.exists(filepath):
        raise AppNotFoundError(f"App with id '{app_id}' not found.")

    try:
        with open(filepath, "r") as f:
            settings = json.load(f)
        return JSONResponse(content=settings)
    except json.JSONDecodeError:
        raise MalformedAppConfigError(f"The configuration file for app '{app_id}' is malformed.")
    except Exception as e:
        raise e


@router.get("/api/apps")
async def get_apps():
    """
    Reads all app example JSON files, extracts key information,
    and returns a list of app configurations.
    """
    apps = []
    try:
        app_files = [f for f in os.listdir(APP_EXAMPLES_PATH) if f.endswith(".json")]

        for i, filename in enumerate(app_files):
            filepath = os.path.join(APP_EXAMPLES_PATH, filename)
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                    apps.append({
                        "id": filename.replace(".json", ""),
                        "name": data.get("app_name", "Unnamed App"),
                        "summary": data.get("agent_description", "No summary available.")
                    })
            except json.JSONDecodeError:
                raise MalformedAppConfigError(f"The configuration file '{filename}' is malformed.")
    except FileNotFoundError:
        raise AppNotFoundError("The apps directory was not found.")
    except Exception as e:
        raise e

    return apps
