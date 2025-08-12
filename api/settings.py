import json
from pydantic import BaseModel
from typing import Dict


DEFAULT_SETTINGS_FILE_PATH = "api/default_settings.json"
APP_EXAMPLES_PATH = "app_examples"
LIVE_MODEL_NAME = "gemini-2.5-flash-live-preview"
IMAGE_MODEL_NAME = "gemini-2.0-flash-preview-image-generation"


class Settings(BaseModel):
    app_name: str
    agent_description: str
    context_dict: Dict[str, dict]
    goal_description: str
    notes_taking_instruction: str
    analyse_instruction: str
    voice_name: str
    language_code: str


def load_default_settings():
    return json.load(open(DEFAULT_SETTINGS_FILE_PATH, "r", encoding="utf-8"))
