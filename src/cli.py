import json

import typer

from log_queue_api import kafka_io
from log_queue_api.json_io import yield_ts_and_uid


app = typer.Typer()


@app.command()
def create_topics():
    kafka_io.create_topics(["website_visits", "visits_per_minute"])


@app.command()
def delete_topics():
    kafka_io.delete_topics(["website_visits", "visits_per_minute"])


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
def subscribe_to_website_visits():
    kafka_io.subscribe("website_visits")


@app.command()
def stream_website_visits(*args, **kwargs):
    for ts, uid in yield_ts_and_uid(path=kwargs.get("path"), limit=kwargs.get("limit")):
        data = json.dumps({
            "ts": ts,
            "uid": uid,
        })
        kafka_io.push("website_visits", ts, data)


if __name__ == "__main__":
    app()
