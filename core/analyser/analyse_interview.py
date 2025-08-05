from google import genai
from google.genai import types


from core.voice_agent.context import load_interviewer_context, InterviewerContext
from core.voice_agent.context import DATA_PATH

def save_analysis(analysis: str) -> str:
    """Saves the analysis to a file in the default context directory.

    Args:
        analysis (str): The analysis text to save.

    Returns:
        str: Confirmation message indicating the analysis was saved.
    """
    with open(f"{DATA_PATH}/interview_analysis.md", "w") as f:
        f.write(analysis)
    return "Analysis saved successfully."


def analyse_interview(
        context: InterviewerContext
) -> None:
    instruction_template = """
    You are an expert interview analyst. Your task is to analyze the provided interview notes
    and generate actionable suggestions based on the candidate's performance, the role description,
    and the job description.

    Role Description:
    {role_description}

    Job Description:
    {job_description}

    Interview Notes:
    {interview_notes}

    Based on the information above, please provide a detailed analysis of the candidate's strengths and weaknesses,
    format in Markdown.
    """

    client = genai.Client(vertexai=False)
    final_instruction = instruction_template.format(
        role_description=context.role_description,
        job_description=context.job_description,
        interview_notes=context.interview_notes
    )
    response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[final_instruction],
    )
    return response.text