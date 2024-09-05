from pathlib import Path
from typing import Generator

from fastapi import FastAPI, File, UploadFile
from starlette.responses import FileResponse, StreamingResponse
from starlette.staticfiles import StaticFiles

from web import explorer, creature, user

app = FastAPI()

app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)

top = Path(__file__).resolve().parent

app.mount("/static",
          StaticFiles(directory=f"{top}/static", html=True),
          name="free")


@app.get("/")
async def root():
    return "top here"


# 파일은 https://myjob.page/tools/test-files 여기서 다운로드

@app.post("/small")
async def upload_small_file(small_file: bytes = File()) -> str:
    return f"file size: {len(small_file)}"


@app.get("/small/{name}")
async def download_small_file(name):
    return FileResponse(name)


def gen_file(path: str) -> Generator:
    with open(file=path, mode="rb") as file:
        yield file.read()


@app.post("/big")
async def upload_big_file(big_file: UploadFile) -> str:
    return f"file size: {big_file.size}, name: {big_file.filename}"


@app.get("/download_big/{name}")
async def download_big_file(name: str):
    gen_expr = gen_file(path=name)
    response = StreamingResponse(
        content=gen_expr,
        status_code=200,
    )
    return response


@app.get("/echo/{thing}")
def echo(thing):
    return f"echoing {thing}"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
