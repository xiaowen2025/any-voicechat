from google import genai
from api.settings import AppSettings, settings

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
    context = {
        k: v["value"]
        for k, v in app_settings.context_dict.items()
        if v.get("value")
    }
    if app_settings.gemini_api_key:
        genai.configure(api_key=app_settings.gemini_api_key)
    client = genai.Client(vertexai=False)
    final_instruction = instruction_template.format(
        analyse_instruction=app_settings.analyse_instruction,
        context=context,
        notes=notes,
    )
    response = client.models.generate_content(
        model=settings.live_model_name,
        contents=[final_instruction],
    )
    return response.text
