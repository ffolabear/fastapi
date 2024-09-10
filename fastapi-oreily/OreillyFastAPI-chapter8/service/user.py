import os
from datetime import timedelta, datetime

import bcrypt
from jose import jwt

from model.user import PublicUser, PrivateUser, SignInUser

if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import user as data
else:
    from data import user as data

# --- 새로운 인증 관련 코드

# SECRET_KEY는 반드시 바꾸고 배포해야한다!
SECRET_KEY = "keep-it-secret-keep-it-safe"
ALGORITHM = "HS256"


def verify_password(plain: str, hash: str) -> bool:
    """plain을 해시 값과 DB 의 hash 값과 비교"""
    password_bytes = plain.encode("utf-8")
    hash_bytes = hash.encode("utf-8")
    is_valid = bcrypt.checkpw(password_bytes, hash_bytes)
    return is_valid


def get_hash(plain: str) -> str:
    """plain 의 해시값을 반환"""
    password_bytes = plain.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode("utf-8")


def get_jwt_username(token: str) -> str | None:
    """JWT 접근 토큰으로부터 username 을 반환한다"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not (usename := payload.get("sub")):
            return None
    except jwt.JWTError:
        return None
    return usename


def get_current_user(token: str) -> PublicUser | None:
    """OAuth 토큰을 풀어서 PublicUser 를 반환한다."""
    if not (usename := get_jwt_username(token)):
        return None
    if (user := lookup_user(usename)):
        return user
    return None


def lookup_user(username: str, is_public: bool) -> PublicUser | PrivateUser | None:
    """DB에서 username 에 매칭되는 User 를 반환
    true = PublicUser
    false = PrivateUser -> hash 속성 가지고 있음 
    """
    if (user := data.get_one(username, is_public=is_public)):
        return user
    return None


def auth_user(name: str, plain: str) -> PublicUser | PrivateUser | None:
    """name 과 plain 암호로 유저를 인증한다."""
    if not (user := lookup_user(name, is_public=False)):
        return None
    if not verify_password(plain, user.hash):
        return None
    return user


def create_access_token(data: dict, expires: timedelta | None = None) -> str:
    """JWT 토큰을 반환한다."""
    src = data.copy()
    now = datetime.now()
    if not expires:
        expires = timedelta(minutes=15)
    src.update({"exp": now + expires})
    encoded_jwt = jwt.encode(src, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# CRUD 통과 코드
def get_all() -> list[PublicUser]:
    return data.get_all()


def get_one(name) -> PublicUser:
    return data.get_one(name)


# data.create 는 hash 속성을 지닌 privateUser 를 기대
# SignUser 의 password 를 해시한 hash 속성을 가지고 있는 privatUser 를 만들어서 전달
def create(sign_in_user: SignInUser) -> PublicUser:
    user = PrivateUser(name=sign_in_user.name, hash=get_hash(sign_in_user.password))
    return data.create(user)


def modify(name: str, user: PublicUser) -> PublicUser:
    return data.modify(name, user)


def delete(name: str) -> None:
    return data.delete(name)
