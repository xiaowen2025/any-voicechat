from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api import api_key
from api.websocket import connection as websocket
from api import analyse
from api import avatar
from api import apps

load_dotenv()

app = FastAPI()

app.include_router(analyse.router)
app.include_router(api_key.router)
app.include_router(websocket.router)
app.include_router(avatar.router)
app.include_router(apps.router)

app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
