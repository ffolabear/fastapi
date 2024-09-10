from contextlib import asynccontextmanager

from fastapi import FastAPI

import uvicorn
from starlette.responses import RedirectResponse

from database.connection import Settings
from routes.events import event_router
from routes.users import user_router

app = FastAPI()
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

settings = Settings()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


@app.on_event("startup")
async def init_db():
    await settings.initialize_database()


@app.get("/")
async def home():
    return RedirectResponse(url="/event")
