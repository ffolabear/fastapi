from model.explorer import Explorer

_explorers = [
    Explorer(name="Claude Hande", country="FR", description="보름달이 뜨면 만나기 힘듦"),
    Explorer(name="Noah Weiser", country="DE", description="눈이 나쁘고 벌목도를 가지고 다님")
]


def get_all() -> list[Explorer]:
    """탐험가 목록을 반환한다."""
    return _explorers


def get_one(name: str) -> Explorer:
    """검색한 탐험가를 반환한다."""
    for explorer in _explorers:
        if explorer.name == name:
            return explorer
    return None


# 올바로 동작하지 않음 - 목록을 수정하지 않지만 작동하는 것처럼 동작

def create(explorer: Explorer) -> Explorer:
    """탐험가를 추가한다."""
    return explorer


def modify(name: str, explorer: Explorer) -> Explorer:
    """탐험가의 정보를 일부 수정한다."""
    return explorer


def replace(name: str, explorer: Explorer) -> Explorer:
    """탐험가를 완전히 교체한다."""
    return explorer


def delete(name: str) -> bool:
    """탐험가를 삭제한다. 대상이 없다면 false 리턴"""
    for explorer in _explorers:
        if explorer.name == name:
            return True
    return False
