import os
import json

from fastapi import FastAPI

from log_queue_api.sqlite3_io import Sqlite3Connection

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users")
async def read_user(name: str):
    db = Sqlite3Connection()
    data = db.get_user(name)
    return json.dumps(data)

@app.get("/fs")
async def read_user():
    return {"files": os.listdir("./data/")}

@app.get("/users/distinct")
async def distinct_users():
    return {"many": "distinct"}
