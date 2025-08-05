import os
from datetime import datetime
import aiofiles


from core.voice_agent.context import DATA_PATH

NOTES_FILE = f"{DATA_PATH}interview_note.md"

async def tool_take_notes(note: str) -> str:
    """
    Update the interview_note.md file with a new Q&A pair.

    Args:
        note (str): The interview question and the candidate's answer formatted as a string.
    Returns:
        None
    """
    # Ensure notes are loaded or initialized
    if not os.path.exists(NOTES_FILE):
        notes = ""
    else:
        async with aiofiles.open(NOTES_FILE, "r", encoding="utf-8") as f:
            notes = await f.read()

    # Append new Q&A
    notes += f"\n## {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{note}\n\n"

    async with aiofiles.open(NOTES_FILE, "w", encoding="utf-8") as f:
        await f.write(notes)

if __name__ == "__main__":
    # Example usage
    # uv run python -m core.voice_agent.tools
    import asyncio
    note = "Q: What is your name?\nA: John Doe."
    updated_notes = asyncio.run(tool_take_notes(note))
    print(updated_notes)