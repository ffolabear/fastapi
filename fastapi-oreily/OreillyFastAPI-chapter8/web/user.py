import os
from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt

from model.user import PublicUser, SignInUser

if os.getenv("CRYPTID_UNIT_KEY"):
    from fake import user as service
else:
    from service import user as service
from error import Missing, Duplicate

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/user")

# --- 새로운 인증 관련 코드들

# 이 의존성은 "/user/token"을 동작하게하고
# (username과 pass를 담고있는 form을 읽는다.)
# 액세스 토큰을 반환한다.

oauth2_dep = OAuth2PasswordBearer(tokenUrl="/user/token")


def unauthed():
    raise HTTPException(
        status_code=401,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/token")
async def create_access_token(
        from_data: OAuth2PasswordRequestForm = Depends()):
    """username 과 password 를 oauth 양식에서 꺼내고 JWT 접근 토큰을 반환"""
    user = service.auth_user(from_data.username, from_data.password)
    if not user:
        unauthed()
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data={"sub": user.name}, expires=expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# 이 엔드 포인트는 oauth2_dep() 의존성을 가지고 있다.
@router.get("/token")
def get_access_token(token: str = Depends(oauth2_dep)) -> dict:
    """현재 접근 토큰을 반환한다."""
    return {"token": token}


# 이전 CRUD 코드
@router.get("/")
def get_all() -> list[PublicUser]:
    return service.get_all()


@router.get("/{name}")
def get_one(name) -> PublicUser:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.post("/", status_code=201)
def create(user: SignInUser) -> PublicUser:
    try:
        return service.create(user)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)


@router.patch("/{name")
def modify(name: str, user: SignInUser) -> PublicUser:
    try:
        return service.modify(name, user)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.delete("/{name")
def delete(name: str) -> None:
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)
