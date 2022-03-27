from typing import List, Optional
import json
from pprint import pprint

import typer

from log_queue_api import kafka_io
from log_queue_api import sqlite3_io

app = typer.Typer()


@app.command()
def init():
    # TODO: Implement args: def init(topics: List[str] = None):
    topics = ["user_events", "org_events"]
    kafka_io.create_topics(topics)
    sqlite3_io.Sqlite3Connection().create_tables()


@app.command()
def teardown():
    topics = ["user_events", "org_events"]
    kafka_io.delete_topics(topics)


@app.command()
def produce(topic: str, key: str, value: str):
    kafka_io.push(topic, key, value)


@app.command()
def subscribe(topic: str):
    kafka_io.subscribe(topic)


@app.command()
def stream_user_events():
    with open("./data/user_events.json") as f:
        j = json.load(f)
    for i in j:
        kafka_io.push("user_events", i["received_at"], json.dumps(i))


@app.command()
def stream_org_events():
    with open("./data/org_events.json") as f:
        j = json.load(f)
    for i in j:
        kafka_io.push("org_events", i["created_at"], json.dumps(i))


if __name__ == "__main__":
    app()
