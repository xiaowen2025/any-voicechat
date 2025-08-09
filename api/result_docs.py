# Result Documents include notes took during conversations and the post-conversation analysis.
import os
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse


from core.settings import DATA_PATH

router = APIRouter()


@router.get("/api/result_docs/{doc_name}")
async def get_document(doc_name: str):
    file_path = os.path.join(DATA_PATH, f"{doc_name}.md")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return JSONResponse(content={"content": content})
    except FileNotFoundError:
        return JSONResponse(content={"error": f"{doc_name} not found."}, status_code=404)

@router.put("/api/result_docs/{doc_name}")
async def update_document(doc_name: str, request: Request):
    file_path = os.path.join(DATA_PATH, f"{doc_name}.md")
    try:
        data = await request.json()
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(data["content"])
        
        return JSONResponse(content={"message": f"{doc_name} updated successfully."})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
