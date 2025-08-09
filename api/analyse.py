# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fastapi import APIRouter, Depends
from core.analyse import analyse, save_analysis
from core.settings import DATA_PATH, Settings
from api.dependencies import get_settings

router = APIRouter()

@router.post("/api/analyse")
async def post_analyse(settings: Settings = Depends(get_settings)):
    notes = open(f"{DATA_PATH}/notes.md", "r").read()
    analysis_result = analyse(settings, notes)
    save_analysis(analysis_result)
    return {"message": "Analysis complete", "analysis": analysis_result}
