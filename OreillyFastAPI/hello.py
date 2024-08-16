from fastapi import FastAPI, Body, Header

app = FastAPI()


@app.get("/hi/{who}")
def greet_url(who):
    return f"Hello? {who}"


@app.get("/hi")
def greet_query_param(who):
    return f"Hello? {who}"


@app.post("/hi")
def greet_body(who: str = Body(embed=True)):
    return f"Hello? {who}"


@app.get("/header")
def greet_header(who: str = Header()):
    return f"Hello? {who}"


@app.get("/agent")
def get_agent(user_agent: str = Header()):
    return user_agent


@app.get("/happy")
def happy(status_code=200):
    return ":)"



if __name__ == "__main__":
    import uvicorn

    uvicorn.run("hello:app", reload=True)
