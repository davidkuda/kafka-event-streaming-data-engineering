from typing import List, Optional

import typer

from log_queue_api import kafka_io

app = typer.Typer()


@app.command()
def init():
# TODO: Implement args: def init(topics: List[str] = None):
    topics = ["user_events", "org_events"]
    kafka_io.create_topics(topics)


@app.command()
def teardown():
    topics = ["user_events", "org_events"]
    kafka_io.delete_topics(topics)


if __name__ == "__main__":
    app()
