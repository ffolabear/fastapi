import os

import pytest

from data import creature
from error import Duplicate, Missing
from model.creature import Creature

os.environ["CRYPTID_SQLITE_DB"] = ":memory:"


@pytest.fixture
def sample() -> Creature:
    return Creature(
        name="yeti",
        description="Harmless Himalayan",
        country="CN",
        area="Himalayas",
        aka="Abominable Snowman",
    )


def test_create(sample):
    resp = creature.create(sample)
    assert resp == sample


def test_create_duplicate(sample):
    with pytest.raises(Duplicate):
        _ = creature.create(sample)


def test_get_one(sample):
    resp = creature.get_one(sample.name)
    assert resp == sample


def test_get_one_missing():
    with pytest.raises(Missing):
        _ = creature.get_one("boxturtle")


def test_modify(sample):
    creature.country = "JP"
    resp = creature.modify(sample.name, sample)
    assert resp == sample


def test_modify_missing(sample):
    thing: Creature = Creature(
        name="snurfle", description="some thing", country="somewhere", area="", aka=""
    )
    with pytest.raises(Missing):
        _ = creature.modify(thing.name, thing)


def test_delete(sample):
    resp = creature.delete(sample.name)
    assert resp is True


def test_delete_missing(sample):
    with pytest.raises(Missing):
        _ = creature.delete(sample.name)
