import json


def yield_ts_and_uid(
    json_file_path: str = "data/doodle_data.json",
    limit: int = 10000,
    skip_equals: bool = True,
):
    """Simulates the stream from the topic on subscribe."""
    counter = 0
    with open(json_file_path, "r") as f:
        counter = 0

        previous_ts: str = None

        for line in f:
            data = json.loads(line)

            if skip_equals:
                if previous_ts == data["ts"]:
                    continue
                else:
                    previous_ts = data["ts"]

            yield data["ts"], data["uid"]

            counter += 1
            if counter == limit:
                break
