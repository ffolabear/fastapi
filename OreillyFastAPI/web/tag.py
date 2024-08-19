from datetime import datetime

from fastapi import FastAPI

import service.tag as service
from model.tag import TagIn, Tag, TagOut

app = FastAPI()


@app.post('/')
def create(tag_in: TagIn) -> TagIn:
    tag: Tag = Tag(tag=tag_in.tag, create=datetime.now(), secret="shhhhh")
    service.create(tag)
    return tag_in


@app.get('/{tag_str}', response_model=TagOut)
def get_one(tag_str: str) -> TagOut:
    tag: Tag = service.get(tag_str)
    return tag