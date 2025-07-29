from pydantic import BaseModel

DATA_PATH = "default_context/"  # Default path for data storage

class InterviewerContext(BaseModel):
    """Configuration for the interviewer agent."""
    role_description: str
    job_description: str
    resume: str
    interview_notes: str

def load_interviewer_context():
    resume_content = open(f"{DATA_PATH}cv.md", "r", encoding="utf-8").read()
    job_description = open(f"{DATA_PATH}job_description.md", "r", encoding="utf-8").read()
    role_description = open(f"{DATA_PATH}role_description.md", "r", encoding="utf-8").read()
    try:
        with open(f"{DATA_PATH}interview_note.md", "r", encoding="utf-8") as f:
            interview_notes = f.read()
    except FileNotFoundError:
        interview_notes = "" # Return empty string if notes don't exist yet

    return InterviewerContext(
        role_description=role_description,
        job_description=job_description,
        resume=resume_content,
        interview_notes=interview_notes
    )

interviewer_context = load_interviewer_context()
