from api.settings import AppSettings


def get_context(app_settings: AppSettings) -> dict:
    """
    Extracts and formats the context from the app_settings.

    Args:
        app_settings (AppSettings): The application settings.

    Returns:
        dict: The formatted context dictionary.
    """
    return {
        k: v["value"]
        for k, v in app_settings.context_dict.items()
        if v.get("value")
    }
