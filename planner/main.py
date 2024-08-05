from contextlib import asynccontextmanager

from fastapi import FastAPI

import uvicorn

from database.connection import conn
from routes.events import event_router
from routes.users import user_router

app = FastAPI()
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


@asynccontextmanager
def on_startup():
    conn()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
