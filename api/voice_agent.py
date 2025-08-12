import logging

from api.services.google_ai import create_live_agent
from api.settings import Settings

instruction_template = """
Role: {agent_description}
Context: {context}
Remember to take the notes: {notes_taking_instruction}
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
        notes_taking_instruction=settings.notes_taking_instruction,
    )

    logging.info(f"Creating agent with context: {final_instruction}")
    return create_live_agent(final_instruction)
