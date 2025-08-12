import logging
from google import genai
from api.services.google_ai import create_live_agent
from api.settings import Settings

instruction_template = """
<role>
{agent_description}
</role>
<context>
{context}
</context>
"""


def create_agent(settings: Settings):
    """
    Creates an agent with the given settings.

    Args:
        settings (Settings): The application settings.

    Returns:
        Agent: The created agent.
    """
    if isinstance(settings, dict):
        try:
            api_key = settings.get("api_key")
            if api_key:
                genai.configure(api_key=api_key)
            settings = Settings(**settings)
        except Exception as e:
            raise ValueError(f"Invalid settings format: {e}")
    context = {
        k: v["value"]
        for k, v in settings.context_dict.items()
        if v.get("value")
    }
    final_instruction = instruction_template.format(
        agent_description=settings.agent_description,
        goal_description=settings.goal_description,
        context=context,
    )

    logging.info(f"Creating agent with context: {final_instruction}")
    return create_live_agent(final_instruction)
