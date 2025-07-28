
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types

# Only run this block for Gemini Developer API
router = APIRouter()

class ApiKey(BaseModel):
    key: str

def _verify_api_key(api_key: str):
    """Verifies the provided Gemini API key."""
    client = genai.Client(api_key=api_key)
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents='Response with 1 only.',
            config=types.GenerateContentConfig(
                system_instruction='I say high, you say low',
                max_output_tokens=3,
                temperature=0.3,
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid API Key: {str(e)}")

@router.post("/api/verify_api_key")
async def verify_api_key(api_key: ApiKey):
    """Endpoint to verify the provided Gemini API key."""
    try:
        _verify_api_key(api_key.key)
        os.environ["GEMINI_API_KEY"] = api_key.key
        return {"status": "success", "message": "API Key verified and set."}
    except HTTPException as e:
        return {"status": "error", "message": str(e.detail)}
