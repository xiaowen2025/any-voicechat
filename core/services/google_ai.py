from google import genai
from google.adk.agents import Agent

from core.settings import Settings
from core.take_notes import tool_take_notes


def analyse_notes(settings: Settings, notes: str) -> str:
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
        model="gemini-1.5-flash",
        contents=[final_instruction],
    )
    return response.text


def create_google_agent(
    instruction: str,
) -> Agent:
    """
    Creates a Google agent.

    Args:
        instruction (str): The instruction for the agent.

    Returns:
        Agent: The created agent.
    """
    agent = Agent(
        name="agent",
        model="gemini-1.5-flash-preview-native-audio-dialog",
        description="Voice Agent",
        instruction=instruction,
        tools=[tool_take_notes],
    )
    return agent
