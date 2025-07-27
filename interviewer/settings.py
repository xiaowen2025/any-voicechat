from pydantic import BaseModel

DATA_PATH = "example/"  # Default path for data storage

class Settings(BaseModel):
    """Configuration for the interviewer agent."""
    role_description: str
    job_description: str
    resume: str

def load_settings():
    resume_content = open(f"{DATA_PATH}cv.md", "r", encoding="utf-8").read()
    job_description = open(f"{DATA_PATH}job_description.md", "r", encoding="utf-8").read()
    role_description = open(f"{DATA_PATH}role_description.md", "r", encoding="utf-8").read()

    return Settings(
        role_description=role_description,
        job_description=job_description,
        resume=resume_content
    )

settings = load_settings()
