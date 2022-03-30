import os
import json

from fastapi import FastAPI

from log_queue_api.sqlite3_io import Sqlite3Connection

app = FastAPI()


@app.get("/")
async def root():
    return "Please send a request to /users?name=Snake"

@app.get("/users")
async def read_user(name: str):
    db = Sqlite3Connection()
    return db.get_user(name)

@app.get("/fs")
async def read_user():
    return {"files": os.listdir("./data/")}

@app.get("/users/distinct")
async def distinct_users():
    return {"many": "distinct"}
