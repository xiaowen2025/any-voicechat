from google import genai
from fastapi import APIRouter, Depends
from pydantic import BaseModel


from api.settings import Settings
from api.dependencies import get_settings


router = APIRouter()

class AnalyseRequest(BaseModel):
    notes: str


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


@router.post("/api/analyse")
async def post_analyse(request: AnalyseRequest, settings: Settings = Depends(get_settings)):
    notes = request.notes
    analysis_result = analyse(settings, notes)
    return {"message": "Analysis complete", "analysis": analysis_result}
