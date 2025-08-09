# Result Documents include notes took during conversations and the post-conversation analysis.
import os
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse


from core.settings import DATA_PATH

router = APIRouter()


@router.get("/api/result_docs/{doc_name}")
async def get_document(doc_name: str):
    file_path = os.path.join(DATA_PATH, f"{doc_name}.md")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"{doc_name} not found.")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return JSONResponse(content={"content": content})

@router.put("/api/result_docs/{doc_name}")
async def update_document(doc_name: str, request: Request):
    file_path = os.path.join(DATA_PATH, f"{doc_name}.md")
    data = await request.json()
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(data["content"])

    return JSONResponse(content={"message": f"{doc_name} updated successfully."})
