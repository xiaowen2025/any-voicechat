from google.adk.agents import Agent

from api.take_notes import tool_take_notes
from api.settings import LIVE_MODEL_NAME


def create_live_agent(
    instruction: str,
) -> Agent:
    agent = Agent(
        name="agent",
        model=LIVE_MODEL_NAME,
        description="Voice Agent",
        instruction=instruction,
        tools=[tool_take_notes],
    )
    return agent
