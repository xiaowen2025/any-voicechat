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

import os
import json

from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api import result_docs
from api import api_key
from api import context
from api.websocket import connection as websocket
from api import analyse
from api import avatar
from api import apps
from core.settings import DATA_PATH


load_dotenv()

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    """Initialise the app settings"""
    data_path = Path(DATA_PATH)
    data_path.mkdir(parents=True, exist_ok=True)

    # Create notes file
    notes_path = data_path / "notes.md"
    if not notes_path.exists():
        notes_path.touch()


app.include_router(analyse.router)
app.include_router(result_docs.router)
app.include_router(api_key.router)
app.include_router(context.router)
app.include_router(websocket.router)
app.include_router(avatar.router)
app.include_router(apps.router)

app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
