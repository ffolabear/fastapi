# DB 와 SQL 로 바꿀떄까지 사용할 가짜 데이터
from error import Missing, Duplicate
from model.creature import Creature

# 데이터베이스와 SQL로 바꿀 때까지 사용할 가짜 데이터
_creatures = [
    Creature(
        name="Yeti",
        country="CN",
        area="Himalayas",
        description="Hirsute Himalayan",
        aka="Abominable snowman",
    ),
    Creature(
        name="Bigfoot",
        description="Yeti's Cousin Eddie",
        country="US",
        area="*",
        aka="Sasquatch"
    ),
]


def get_all() -> list[Creature]:
    print("fake")
    """생명체 목록을 반환"""
    return _creatures


def get_one(name: str) -> Creature | None:
    """검색한 생명체를 반환"""
    for _creature in _creatures:
        if _creature.name == name:
            return _creature
    raise Missing(msg=f"Creature {name} not found")


# 올바로 동작하지 않음 - 목록을 수정하지 않지만 작동하는 것처럼 동작

def create(creature: Creature) -> Creature:
    """생명체를 추가"""
    if next((x for x in _creatures if x.name == creature.name), None):
        raise Duplicate(msg=f"Creature {creature.name} already exists")
    _creatures.append(creature)
    return creature


def modify(name: str, creature: Creature) -> Creature:
    """생명체의 정보를 일부 수정한다."""
    _creature = next((x for x in _creatures if x.name == creature.name), None)
    if _creature is not None:
        _creature = creature
        return creature
    raise Missing(msg=f"Creature {creature.name} not found")


def replace(name: str, creature: Creature) -> Creature:
    """생명체를 완전히 교체"""
    _creature = next((x for x in _creatures if x.name == creature.name), None)
    if _creature is None:
        raise Missing(msg=f"Creature {creature.name} not found")

    _creature = creature
    return _creature


def delete(name: str) -> bool:
    """생명체를 삭제한다. 대상이 없다면 false 리턴"""
    if not name:
        return False

    _creature = next((x for x in _creatures if x.name == name), None)
    if _creature is None:
        raise Missing(msg=f"Creature {name} not found")
    _creatures.remove(_creature)
    return True
