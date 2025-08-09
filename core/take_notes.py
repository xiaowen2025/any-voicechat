import os
from datetime import datetime
import aiofiles

from core.settings import DATA_PATH


async def tool_take_notes(note: str) -> str:
    """
    Take notes during the conversation.

    Args:
        note (str): The notes in string format to be saved.
    Returns:
        None
    """
    notes_file_path = f"{DATA_PATH}/notes.md"
    # Ensure notes are loaded or initialized
    if not os.path.exists(notes_file_path):
        notes = ""
    else:
        async with aiofiles.open(notes_file_path, "r", encoding="utf-8") as f:
            notes = await f.read()

    # Append new Q&A
    notes += f"\n## {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{note}\n\n"

    async with aiofiles.open(notes_file_path, "w", encoding="utf-8") as f:
        await f.write(notes)

if __name__ == "__main__":
    # uv run python -m core.voice_agent.take_notes
    import asyncio
    note = "Q: What is your name?\nA: John Doe."
    updated_notes = asyncio.run(tool_take_notes(note))