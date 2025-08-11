from core.config import DATA_PATH
from core.services.google_ai import analyse_notes
from core.settings import Settings


def save_analysis(analysis: str) -> str:
    """
    Saves the analysis to a file.

    Args:
        analysis (str): The analysis text to be saved.

    Returns:
        str: A message indicating the result.
    """
    with open(f"{DATA_PATH}/analysis.md", "w") as f:
        f.write(analysis)
    return "Analysis saved successfully."


def analyse(settings: Settings, notes: str) -> str:
    """
    Analyzes the notes and returns the analysis.

    Args:
        settings (Settings): The application settings.
        notes (str): The notes to be analyzed.

    Returns:
        str: The analysis text.
    """
    return analyse_notes(settings, notes)