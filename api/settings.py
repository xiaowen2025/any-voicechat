from pydantic_settings import BaseSettings
from typing import Dict, Optional

class AppSettings(BaseSettings):
    app_name: str
    agent_description: str
    context_dict: Dict[str, dict]
    goal_description: str
    analyse_instruction: str
    voice_name: str
    language_code: str
    gemini_api_key: Optional[str] = None
    search_tool: Optional[bool] = False

class GlobalSettings(BaseSettings):
    default_app_id: str = "language_pal"
    app_settings_path: str = "app_settings"
    live_model_name: str = "gemini-2.5-flash-live-preview"
    image_model_name: str = "gemini-2.0-flash-preview-image-generation"
    analyse_model_name: str = "gemini-2.5-flash"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = GlobalSettings()
