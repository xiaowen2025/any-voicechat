from google.adk.agents import Agent

from api.settings import LIVE_MODEL_NAME


def create_live_agent(
    instruction: str,
    tools: list
) -> Agent:

    agent = Agent(
        name="agent",
        model=LIVE_MODEL_NAME,
        description="Voice Agent",
        instruction=instruction,
        tools=tools,
    )
    return agent
