from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from api.dependencies import load_settings, save_settings

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


@router.post("/api/settings")
async def update_settings(request: Request):
    """
    Updates the entire settings dictionary.
    """
    try:
        new_settings = await request.json()
        save_settings(new_settings)
        return JSONResponse(content={"message": "Settings updated successfully."})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.get("/api/context")
async def get_context(settings: dict = Depends(load_settings)):
    """
    Retrieves the context dictionary from the settings.
    """
    context = settings.get("context_dict", {})
    return JSONResponse(content=context)


@router.put("/api/context/{context_name}")
async def update_context(context_name: str, request: Request, settings: dict = Depends(load_settings)):
    """
    Updates a specific context entry with a new value.
    """
    data = await request.json()
    value = data.get("value")

    if value is None:
        return JSONResponse(
            content={"error": "'value' is required in request body"}, status_code=400
        )

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
