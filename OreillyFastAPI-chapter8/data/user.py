from error import Missing, Duplicate
from model.user import PublicUser, PrivateUser
from .init import (conn, curs, get_db, IntegrityError)

curs.execute(
    """create table if not exists
                user(
                  name text primary key,
                  hash text)"""
)
curs.execute(
    """create table if not exists
                xuser(
                  name text primary key,
                  hash text)"""
)


# isPublic 인자에 따라 나가는 모델이 분기
def row_to_model(row: tuple, is_public: bool = True) -> PublicUser | PrivateUser:
    name, hash = row
    if is_public:
        return PublicUser(name=name)
    else:
        return PrivateUser(name=name, hash=hash)


def model_to_dict(user: PrivateUser) -> dict:
    return user.model_dump()


# is_public 에 띠리 PublicUser 또는 PrivateUser 반환
def get_one(name: str, is_public: bool = True) -> PublicUser | PrivateUser:
    qry = "select * from user where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row, is_public)
    else:
        raise Missing(msg=f"User {name} not found")


# 유저 목록 조회 에서는 민간 정보를 포함할 일이 없어 PublicUser 모델 집합을 반환
def get_all() -> list[PublicUser]:
    qry = "select * from user"
    curs.execute(qry)
    return [row_to_model(row) for row in curs.fetchall()]


def create(user: PrivateUser, table: str = "user") -> PublicUser:
    """user 테이블 또는 xuser 테이블에 유저를 생성한다"""
    qry = f"""insert into {table}
        (name, hash)
        values
        (:name, :hash)"""
    params = model_to_dict(user)
    try:
        curs.execute(qry, params)
    except IntegrityError:
        raise Duplicate(msg=f"User {user.name} already exists")
    return PublicUser(name=user.name)


def modify(name: str, user: PublicUser) -> PublicUser:
    """name으로 조회한 유저의 이름을 수정한다"""
    qry = """update user set
             name=:name
             where name=:name0"""
    params = {"name": user.name, "name0": name}
    curs.execute(qry, params)
    if curs.rowcount == 1:
        return get_one(name)
    raise Missing(msg=f"User {name} not found")


def delete(name: str) -> None:
    """name으로 user 테이블에서 조회한 유저를 삭제하고, xuser 테이블에 추가한다"""
    user = get_one(name, is_public=False)
    qry = "delete from user where name = :name"
    params = {"name": name}
    curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"User {name} not found")
    create(user, table="xuser")

