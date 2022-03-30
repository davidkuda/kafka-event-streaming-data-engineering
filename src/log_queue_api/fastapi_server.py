from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users")
async def read_user(name: str):
    return {"name": "name"}

@app.get("/users/distinct")
async def distinct_users():
    return {"many": "distinct"}
