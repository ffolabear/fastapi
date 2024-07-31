from fastapi import FastAPI

from todo import todo_router

app = FastAPI()         # 초기화


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


@app.get("/")
async def welcome() -> dict:
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


app.include_router(todo_router)
from fastapi import FastAPI

from todo import todo_router

app = FastAPI()         # 초기화


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


@app.get("/")
async def welcome() -> dict:
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


app.include_router(todo_router)
