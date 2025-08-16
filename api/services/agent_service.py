from google.adk.agents import Agent

from api.settings import settings


def create_gemini_live_agent(
    instruction: str,
    tools: list,
    name: str = "Vox",
    description: str = "Most brilliant AI",
) -> Agent:
    agent = Agent(
        name=name,
        model=settings.live_model_name,
        description=description,
        instruction=instruction,
        tools=tools,
    )
    return agent
