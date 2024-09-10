from fastapi import FastAPI

import data
from model.model import Creature

app = FastAPI()


@app.get("/creature")
def get_all() -> list[Creature]:
    return data.get_creatures()
