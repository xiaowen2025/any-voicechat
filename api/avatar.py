import base64
from google import genai
import os
from google.genai import types

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .settings import Settings

router = APIRouter()

class AvatarRequest(BaseModel):
    settings: Settings

def generate_image(prompt: str, api_key: str) -> dict:
    client = genai.Client(api_key=api_key)
    
    model = "gemini-2.0-flash-preview-image-generation"
    
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=str(prompt)),
            ],
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
    )

    image_data = b""
    text_response = ""
    
    response_iterator = client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    for chunk in response_iterator:
        if (
            chunk.candidates is None
            or not chunk.candidates 
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            continue
        
        for part in chunk.candidates[0].content.parts:
            if part.inline_data and part.inline_data.data:
                image_data += part.inline_data.data
        
        if chunk.text:
            text_response += chunk.text
    
    if not image_data:
        if text_response:
            raise Exception(f"Image generation failed: {text_response.strip()}")
        raise Exception("Image generation failed, no image data received.")

    encoded_image = base64.b64encode(image_data).decode("utf-8")

    return {"image": encoded_image}

@router.post("/api/avatar/generate")
async def generate_avatar(req: AvatarRequest):
    try:
        prompt = f"Design a minimalist cartoon avatar for {req.settings.agent_description}. Considering the context: {req.settings.context_dict}"
        return generate_image(prompt, api_key=req.settings.gemini_api_key)
    except Exception as e:
        error_message = "Sorry, this feature is not available now."
        if "404" in str(e):
            error_message = "gemini-2.0-flash-preview-image-generation is only supported in limited regions."
        raise HTTPException(status_code=500, detail=error_message)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    r = generate_image("a cute cat")
    # save as avatar.png
    with open("avatar.png", "wb") as f:
        f.write(base64.b64decode(r["image"]))
