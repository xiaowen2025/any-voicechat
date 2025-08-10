import json
import os
from pydantic import BaseModel
from typing import Dict

DATA_PATH = "api/._local"
SETTINGS_FILE_PATH = os.path.join(DATA_PATH, "settings.json")
DEFAULT_SETTINGS_FILE_PATH = "core/default_settings.json"


class Settings(BaseModel):
    app_name: str
    agent_description: str
    context_dict: Dict[str, dict]
    goal_description: str
    notes_taking_instruction: str
    analyse_instruction: str
    voice_name: str
    language_code: str


def load_settings():
    """
    Loads settings from the settings file.
    If the file doesn't exist, it creates it from the default settings.
    """
    if not os.path.exists(SETTINGS_FILE_PATH):
        # Create the directory if it doesn't exist
        os.makedirs(DATA_PATH, exist_ok=True)
        # Copy default settings to the new settings file
        with open(DEFAULT_SETTINGS_FILE_PATH, "r", encoding="utf-8") as f_default:
            default_settings = json.load(f_default)
        with open(SETTINGS_FILE_PATH, "w", encoding="utf-8") as f_settings:
            json.dump(default_settings, f_settings, indent=4)
        return default_settings
    else:
        with open(SETTINGS_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)


def save_settings(settings: dict):
    """
    Saves the given settings to the settings file.
    """
    with open(SETTINGS_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)


# Load default settings for validation and type hinting if needed elsewhere
try:
    default_settings = load_settings()
except (FileNotFoundError, json.JSONDecodeError):
    # Handle cases where default settings might be corrupted or not found
    # during initial setup, though load_settings should prevent this.
    print("Warning: Could not load default settings.")
    default_settings = {}
