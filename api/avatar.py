import base64
from google import genai
import os
from google.genai import types
from google.api_core import exceptions as google_exceptions

from fastapi import APIRouter
from pydantic import BaseModel

from .settings import Settings
from .exceptions import ApiKeyError, ImageGenerationError

router = APIRouter()

class AvatarRequest(BaseModel):
    settings: Settings

def generate_image(prompt: str, api_key: str) -> dict:
    if not api_key:
        raise ApiKeyError("Gemini API key is not provided.")

    try:
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
                raise ImageGenerationError(f"Image generation failed: {text_response.strip()}")
            raise ImageGenerationError("Image generation failed, no image data received.")

        encoded_image = base64.b64encode(image_data).decode("utf-8")

        return {"image": encoded_image}
    except google_exceptions.GoogleAPICallError as e:
        if "api key" in str(e).lower():
            raise ApiKeyError(f"Invalid Gemini API key: {e}")
        raise ImageGenerationError(f"Google API call error: {e}")
    except Exception as e:
        raise ImageGenerationError(f"An unexpected error occurred during image generation: {e}")

@router.post("/api/avatar/generate")
async def generate_avatar(req: AvatarRequest):
    prompt = f"Design a minimalist cartoon avatar for {req.settings.agent_description}. Considering the context: {req.settings.context_dict}"
    return generate_image(prompt, api_key=req.settings.gemini_api_key)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    r = generate_image("a cute cat")
    # save as avatar.png
    with open("avatar.png", "wb") as f:
        f.write(base64.b64decode(r["image"]))
