import asyncio
from google.adk.agents import Agent

from core.voice_agent.take_notes import tool_take_notes
from core.voice_agent.prompt import instruction_template
from core.voice_agent.context import load_interviewer_context

def create_agent() -> Agent:
    """Creates and returns an interviewer agent."""

    interviewer_context = load_interviewer_context()
    final_instruction = instruction_template.format(
        role_description=interviewer_context.role_description,
        job_description=interviewer_context.job_description,
        resume=interviewer_context.resume
    )

    root_agent = Agent(
        name="interview_agent",
        # model="gemini-2.5-flash-preview-native-audio-dialog",
        model="gemini-live-2.5-flash-preview",  # Replace with the latest supported model ID
        description="Interviewer",
        instruction=final_instruction,
        tools=[tool_take_notes],
    )
    return root_agent
