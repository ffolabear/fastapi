from fastapi import APIRouter, HTTPException

from error import Missing, Duplicate
from model.creature import Creature
import service.creature as service

router = APIRouter(prefix="/creature")


@router.get("")
@router.get("/")
def get_all() -> list[Creature]:
    return service.get_all()


@router.get("/{name}")
@router.get("/{name}/")
def get_one(name) -> Creature | None:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


# 현재는 아무 일도 하지 않음
@router.post("", status_code=201)
@router.post("/", status_code=201)

def create(creature: Creature) -> Creature:
    try:
        return service.create(creature)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.patch("/{name}")
def modify(name, creature: Creature) -> Creature:
    return service.modify(name, creature)


@router.put("/{name}")
def replace(name, creature: Creature) -> Creature:
    return service.replace(name, creature)


@router.delete("/{name}")
def delete(name: str):
    return service.delete(name)
