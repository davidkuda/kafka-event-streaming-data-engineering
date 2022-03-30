import json

import typer

from log_queue_api import kafka_io
from log_queue_api import sqlite3_io
from log_queue_api.event_handlers import handle_org_events, handle_user_events


app = typer.Typer()


@app.command()
def init():
    topics = ["user_events", "org_events"]
    kafka_io.create_topics(topics)
    db = sqlite3_io.Sqlite3Connection()
    db.create_tables()


@app.command()
def teardown():
    topics = ["user_events", "org_events"]
    kafka_io.delete_topics(topics)
    db = sqlite3_io.Sqlite3Connection()
    db.remove_existing_db_file()


@app.command()
def list_topics():
    kafka_io.list_topics()


@app.command()
def produce(topic: str, key: str, value: str):
    kafka_io.push(topic, key, value)


@app.command()
def subscribe(topic: str):
    kafka_io.subscribe(topic)


@app.command()
def listen_to_user_events():
    kafka_io.subscribe("user_events", handle_user_events)


@app.command()
def listen_to_org_events():
    kafka_io.subscribe("org_events", handle_org_events)


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
