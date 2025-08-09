import json
from google.adk.agents import Agent


from core.take_notes import tool_take_notes
from core.prompt import instruction_template
from core.settings import Settings, default_settings
import logging


def create_agent(settings) -> Agent:
    if isinstance(settings, dict):
        try:
            settings = Settings(**settings)
        except Exception as e:
            raise ValueError(f"Invalid settings format: {e}")
    context = {k:v["value"] for k, v in settings.context_dict.items() if v.get("value")}
    final_instruction = instruction_template.format(
        agent_description=settings.agent_description,
        goal_description=settings.goal_description,
        context=context,
        notes_taking_instruction=settings.notes_taking_instruction,
    )

    logging.info(f"Creating agent with context: {final_instruction}")
    root_agent = Agent(
        name="agent",
        # model="gemini-2.5-flash-preview-native-audio-dialog",
        model="gemini-live-2.5-flash-preview",  
        description="Voice Agent",
        instruction=final_instruction,
        tools=[tool_take_notes],
    )
    return root_agent

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    agent = create_agent(default_settings)