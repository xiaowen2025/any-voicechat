import logging
import os
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

instruction_template = """You are the most brilliant AI that always adapt to the human's needs.

The human has configured the following behavior that you should follow: {agent_description}  

And here is the context of the conversation: 
{context}  

You can use the edit_context_dict tool to update the context dictionary when needed.
"""

def create_agent(
        settings: Settings,
        tools: list
    ):
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
    )

    logging.info(f"Creating agent with context: {final_instruction}")
    if settings.gemini_api_key:
        os.environ["GEMINI_API_KEY"] = settings.gemini_api_key
    return create_live_agent(
        final_instruction,
        tools=tools
    )
