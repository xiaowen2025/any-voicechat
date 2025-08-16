import os
import json
from typing import List, Dict, Any

from api.settings import settings
from ..exceptions import AppNotFoundError, MalformedAppConfigError

def get_app_settings(app_id: str) -> Dict[str, Any]:
    """
    Retrieves the settings for a specific app.
    """
    filepath = os.path.join(settings.app_settings_path, f"{app_id}.json")
    if not os.path.exists(filepath):
        raise AppNotFoundError(f"App with id '{app_id}' not found.")

    try:
        with open(filepath, "r") as f:
            app_settings = json.load(f)
        return app_settings
    except json.JSONDecodeError:
        raise MalformedAppConfigError(f"The configuration file for app '{app_id}' is malformed.")

def get_apps() -> List[Dict[str, Any]]:
    """
    Reads all app example JSON files, extracts key information,
    and returns a list of app configurations.
    """
    apps = []
    try:
        app_files = [f for f in os.listdir(settings.app_settings_path) if f.endswith(".json")]

        for filename in app_files:
            filepath = os.path.join(settings.app_settings_path, filename)
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

    return apps
