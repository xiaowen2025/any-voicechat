from google.adk.agents import Agent
from google.adk.tools import google_search  

from api.settings import LIVE_MODEL_NAME


def create_live_agent(
    instruction: str,
    search_tool: bool,
) -> Agent:

    tools = []
    if search_tool:
        tools.append(google_search)

    agent = Agent(
        name="agent",
        model=LIVE_MODEL_NAME,
        description="Voice Agent",
        instruction=instruction,
        tools=tools,
    )
    return agent
