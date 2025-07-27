import os
from datetime import datetime
import aiofiles


from interviewer.settings import DATA_PATH

NOTES_FILE = f"{DATA_PATH}interview-note.md"

async def tool_take_notes(question_and_answer: str) -> str:
    """
    Update or create the interview-note.md file with a new Q&A pair.

    Args:
        question_and_answer (str): The interview question and answer.

    Returns:
        str: Updated contents of the interview note.
    """
    # Ensure notes are loaded or initialized
    if not os.path.exists(NOTES_FILE):
        notes = "# Interview Notes\n\n"
    else:
        async with aiofiles.open(NOTES_FILE, "r", encoding="utf-8") as f:
            notes = await f.read()

    # Append new Q&A
    notes += f"\n## {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{question_and_answer}\n\n"

    async with aiofiles.open(NOTES_FILE, "w", encoding="utf-8") as f:
        await f.write(notes)
    
if __name__ == "__main__":
    # Example usage
    # uv run python -m interviewer.tools
    import asyncio
    question_and_answer = "Q: What is your name?\nA: John Doe."
    updated_notes = asyncio.run(tool_take_notes(question_and_answer))
    print(updated_notes)