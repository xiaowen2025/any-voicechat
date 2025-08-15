import json
from pydantic import BaseModel
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()


DEFAULT_SETTINGS_FILE_PATH = "api/default_settings.json"
APP_SETTINGS_PATH = "app_settings"
LIVE_MODEL_NAME = "gemini-2.5-flash-live-preview"
IMAGE_MODEL_NAME = "gemini-2.0-flash-preview-image-generation"


class Settings(BaseModel):
    app_name: str
    agent_description: str
    context_dict: Dict[str, dict]
    goal_description: str
    analyse_instruction: str
    voice_name: str
    language_code: str
    gemini_api_key: Optional[str] = None
    search_tool: Optional[bool] = False


def load_default_settings():
    return json.load(open(DEFAULT_SETTINGS_FILE_PATH, "r", encoding="utf-8"))
