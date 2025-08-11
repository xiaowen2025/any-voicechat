import json
from api.settings import (
    DATA_PATH,
    Settings,
    load_settings as core_load_settings,
    save_settings as core_save_settings,
)


def get_settings():
    settings = json.loads(open(f"{DATA_PATH}/settings.json").read())
    return Settings(**settings)


def load_settings():
    return core_load_settings()


def save_settings(settings: dict):
    core_save_settings(settings)
