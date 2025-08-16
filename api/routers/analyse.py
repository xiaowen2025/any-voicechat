from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from api.settings import AppSettings
from api.services import analysis_service

router = APIRouter()

class AnalyseRequest(BaseModel):
    notes: str
    settings: Optional[AppSettings] = None

@router.post("/api/analyse")
async def post_analyse(
    request: AnalyseRequest,
):
    analysis_result = analysis_service.analyse_notes(request.settings, request.notes)
    return {"message": "Analysis complete", "analysis": analysis_result}
