import logging
import os
from google import genai
from api.services.agent_service import create_gemini_live_agent
from api.settings import AppSettings

instruction_template = """You are the most brilliant AI that always adapt to the human's needs.

The human has configured the following behavior that you should follow: {agent_description}

Your goal is to: {goal_description}

And here is the context of the conversation:
{context}

You can use the edit_context_dict tool to update the context dictionary when needed.
"""

def create_agent(
        app_settings: AppSettings,
        tools: list
    ):
    if isinstance(app_settings, dict):
        try:
            app_settings = AppSettings(**app_settings)
        except Exception as e:
            raise ValueError(f"Invalid settings format: {e}")
    context = {
        k: v["value"]
        for k, v in app_settings.context_dict.items()
        if v.get("value")
    }
    final_instruction = instruction_template.format(
        agent_description=app_settings.agent_description,
        goal_description=app_settings.goal_description,
        context=context,
    )

    logging.info(f"Creating agent with context: {final_instruction}")
    if app_settings.gemini_api_key:
        os.environ["GOOGLE_API_KEY"] = app_settings.gemini_api_key
    return create_gemini_live_agent(
        final_instruction,
        tools=tools
    )
