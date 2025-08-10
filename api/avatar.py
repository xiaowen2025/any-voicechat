import base64
import google.generativeai as genai
import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from google.genai.types import GenerateImagesConfig

router = APIRouter()

class AvatarRequest(BaseModel):
    prompt: str

@router.post("/api/avatar/generate")
async def generate_avatar(req: AvatarRequest):
    try:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])

        client = genai.Client()

        image = client.models.generate_images(
            model="imagen-3.0-generate-001",
            prompt=req.prompt,
            config=GenerateImagesConfig(
                image_size="2K",
            ),
        )

        image_bytes = image.generated_images[0].image.image_bytes
        encoded_image = base64.b64encode(image_bytes).decode("utf-8")

        return {"image": encoded_image}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
