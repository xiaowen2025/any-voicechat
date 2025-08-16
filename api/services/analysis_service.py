from google import genai
from api.settings import AppSettings, settings
from api.utils import get_context


def analyse_notes(app_settings: AppSettings, notes: str) -> str:
    """
    Analyzes the notes using the Gemini AI model.

    Args:
        app_settings (AppSettings): The application settings.
        notes (str): The notes to be analyzed.

    Returns:
        str: The analysis text.
    """
    instruction_template = """
    Task:
    {analyse_instruction}
    Context:
    {context}
    Transcription (message after "You" is what the user said):
    {notes}
    """
    context = get_context(app_settings)
    if app_settings.gemini_api_key:
        client = genai.Client(api_key=app_settings.gemini_api_key)
    else:
        client = genai.Client()
    final_instruction = instruction_template.format(
        analyse_instruction=app_settings.analyse_instruction,
        context=context,
        notes=notes,
    )
    response = client.models.generate_content(
        model=settings.analyse_model_name,
        contents=[final_instruction],
    )
    return response.text
