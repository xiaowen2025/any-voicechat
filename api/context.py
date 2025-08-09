from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from core.settings import load_settings, save_settings

router = APIRouter()


@router.get("/api/settings")
async def get_settings():
    """
    Retrieves the entire settings dictionary.
    """
    try:
        settings = load_settings()
        return JSONResponse(content=settings)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.get("/api/context")
async def get_context():
    """
    Retrieves the context dictionary from the settings.
    """
    try:
        settings = load_settings()
        context = settings.get("context_dict", {})
        return JSONResponse(content=context)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.put("/api/context/{context_name}")
async def update_context(context_name: str, request: Request):
    """
    Updates a specific context entry with a new value.
    """
    try:
        data = await request.json()
        value = data.get("value")

        if value is None:
            return JSONResponse(
                content={"error": "'value' is required in request body"}, status_code=400
            )

        settings = load_settings()
        if (
            "context_dict" not in settings
            or context_name not in settings["context_dict"]
        ):
            return JSONResponse(
                content={"error": f"Context '{context_name}' not found."},
                status_code=404,
            )

        settings["context_dict"][context_name]["value"] = value
        save_settings(settings)

        return JSONResponse(
            content={"message": f"Context '{context_name}' updated successfully."}
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
