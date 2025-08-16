from google.adk.agents import Agent

from api.settings import LIVE_MODEL_NAME


def gemini_live_agent(
    instruction: str,
    tools: list
) -> Agent:
    agent = Agent(
        name="Vox",
        model=LIVE_MODEL_NAME,
        description="Most briliiant AI",
        instruction=instruction,
        tools=tools,
    )
    return agent
