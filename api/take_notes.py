import os
import aiofiles

from api.settings import DATA_PATH


async def tool_take_notes(note: str) -> str:
    """
    Take notes during the conversation.

    Args:
        note (str): The notes in string format to be saved.
    Returns:
        str: A message indicating the result.
    """
    notes_file_path = f"{DATA_PATH}/notes.md"
    try:
        # Ensure notes are loaded or initialized
        if not os.path.exists(notes_file_path):
            notes = ""
        else:
            async with aiofiles.open(notes_file_path, "r", encoding="utf-8") as f:
                notes = await f.read()

        notes += f"\n\n{note}"

        async with aiofiles.open(notes_file_path, "w", encoding="utf-8") as f:
            await f.write(notes)
        return "Notes taken successfully."
    except Exception as e:
        return f"Error taking notes: {e}"