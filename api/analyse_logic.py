
from google import genai

from api.settings import DATA_PATH
from api.settings import Settings


def save_analysis(analysis: str) -> str:
    """
    Saves the analysis to a file.

    Args:
        analysis (str): The analysis text to be saved.

    Returns:
        str: A message indicating the result.
    """
    with open(f"{DATA_PATH}/analysis.md", "w") as f:
        f.write(analysis)
    return "Analysis saved successfully."


def analyse(settings: Settings, notes: str) -> str:
    """
    Analyzes the notes using the Gemini AI model.

    Args:
        settings (Settings): The application settings.
        notes (str): The notes to be analyzed.

    Returns:
        str: The analysis text.
    """
    instruction_template = """
    Task:
    {analyse_instruction}
    Context:
    {context}
    Notes:
    {notes}
    """
    context = {
        k: v["value"]
        for k, v in settings.context_dict.items()
        if v.get("value")
    }
    client = genai.Client(vertexai=False)
    final_instruction = instruction_template.format(
        analyse_instruction=settings.analyse_instruction,
        context=context,
        notes=notes,
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[final_instruction],
    )
    return response.text