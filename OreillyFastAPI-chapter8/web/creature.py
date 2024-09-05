import os
from collections import Counter

import country_converter
from fastapi import APIRouter, HTTPException, Response
from plotly import express

from error import Missing, Duplicate
from model.creature import Creature

if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import creature as service
else:
    import service.creature as service

router = APIRouter(prefix="/creature")


@router.get("/")
def get_all() -> list[Creature]:
    return service.get_all()


@router.get("/{name}")
def get_one(name) -> Creature:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.post("/", status_code=201)
def create(creature: Creature) -> Creature:
    try:
        return service.create(creature)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)


@router.patch("/{name}")
def modify(name: str, creature: Creature) -> Creature:
    try:
        return service.modify(name, creature)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.put("/{name}")
def replace(name: str, creature: Creature) -> Creature:
    try:
        return service.replace(name, creature)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.delete("/{name}")
def delete(name: str) -> bool:
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.get("/test/")
def test():
    df = express.data.iris()
    fig = express.scatter(df, x="sepal_width", y="sepal_length", color="species")
    fig_bytes = fig.to_image(format="png")
    return Response(content=fig_bytes, media_type="image/png")


@router.get("/plot/")
def plot():
    creatures = get_all()
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    counts = Counter(creature.name[0] for creature in creatures)
    y = {letter: counts.get(letter, 0) for letter in letters}
    fig = express.histogram(x=list(letters), y=y, title="Creatures Names", labels={"x": "Initial", "y": "Initial"})
    fig_bytes = fig.to_image(format="png")
    return Response(content=fig_bytes, media_type="image/png")


@router.get("/map/")
def map():
    creatures = service.get_all()
    iso2_code = set(creature.country for creature in creatures)
    iso3_code = country_converter.convert(names=iso2_code, to="ISO3")
    fig = express.choropleth(
        locationmode="ISO-3",
        locations=iso3_code)
    fig_bytes = fig.to_image(format="png")
    return Response(content=fig_bytes, media_type="image/png")


@router.get("/map2/")
def map2():
    creatures = service.get_all()
    areas = [creature.area for creature in creatures]
    fig = express.choropleth(
        locationmode="USA-states",
        locations=areas)
    fig_bytes = fig.to_image(format="png")
    return Response(content=fig_bytes, media_type="image/png")
