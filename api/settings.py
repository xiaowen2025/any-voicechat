import os
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

DEFAULT_APP_ID = "language_pal"
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

class JWTSettings(BaseModel):
    secret_key: str = os.getenv("JWT_SECRET_KEY", "a_very_secret_key")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

jwt_settings = JWTSettings()
