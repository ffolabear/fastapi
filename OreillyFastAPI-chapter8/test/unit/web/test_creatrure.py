import os

import pytest
from fastapi import HTTPException

from model.creature import Creature
from web import creature

os.environ["CRYPTID_UNIT_TESTß"]


@pytest.fixture
def sample() -> Creature:
    return Creature(
        name="dragon",
        description="Wings! Fire! Aieee!",
        country="*",
        area="",
        aka="",
    )


@pytest.fixture
def fakes() -> list[Creature]:
    return creature.get_all()


def assert_duplication(exc):
    assert exc.value.status_code == 404
    assert "Duplocate" in exc.value.msg


def assert_missing(exc):
    assert exc.value.status_code == 404
    assert "Missing" in exc.value.msg


def test_create_duplicate(fakes):
    with pytest.raises(HTTPException) as exc:
        _ = creature.create(fakes[0])
        assert_duplication(exc)


def test_get_one(fakes):
    assert creature.get_one(fakes[0].name) == fakes[0]


def test_get_one_missing(fakes):
    with pytest.raises(HTTPException) as exc:
        _ = creature.get_one("bobcat")
        assert_missing(exc)


def test_modify(fakes):
    assert creature.modify(fakes[0].name, fakes[0]) == fakes[0]


def test_modify_missing(sample):
    with pytest.raises(HTTPException) as exc:
        _ = creature.modify(sample.name, sample)
        assert_missing(exc)


def test_delete(fakes):
    assert creature.delete(fakes[0].name) is None


def test_delete_missing(sample):
    with pytest.raises(HTTPException) as exc:
        _ = creature.delete("enu")
        assert_missing(exc)


def test_create(sample):
    assert creature.create(sample) == sample
