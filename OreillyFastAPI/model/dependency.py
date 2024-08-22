from fastapi import FastAPI, Query, Depends

app = FastAPI


def user_dep(name: str = Query(...), gender: str = Query(...), age: int = Query(...)):
    return {"name": name, "valid": True}


def check_dep(name: str = Query(...), gender: str = Query(...)):
    if not name:
        raise


@app.get("/user")
def get_user(user: dict = Depends(user_dep)) -> dict:
    return user


@app.get("/check_user", dependencies=[Depends(check_dep)])
def check_user() -> bool:
    return True