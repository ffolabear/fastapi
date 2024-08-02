from fastapi import FastAPI

import uvicorn

from routes.users import user_router

app = FastAPI()
app.include_router(user_router, prefix="/user")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
