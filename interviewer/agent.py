import asyncio
from google.adk.agents import Agent

from interviewer.tools import tool_take_notes
from interviewer.prompt import instruction_template
from interviewer.settings import load_settings

def create_agent():
    settings = load_settings()
    final_instruction = instruction_template.format(
        role_description=settings.role_description,
        job_description=settings.job_description,
        resume=settings.resume
    )

    root_agent = Agent(
        name="interview_agent",
        model="gemini-live-2.5-flash-preview",  # Replace with the latest supported model ID
        description="Interviewer",
        instruction=final_instruction,
        tools=[tool_take_notes],
    )
    return root_agent
