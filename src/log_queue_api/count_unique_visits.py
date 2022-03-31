from pprint import pprint
from datetime import datetime
import json


def main(window_size: int = 60):
    """Counts unique uids within window_size in seconds.

    Args:
        window_size (int):
            Time range of the unique counts.
            Example: If window_size = 60, count unique uids in one minute.
    """
    window = {}
    window_count = 0
    previous_ts: int = 1
    for ts, uid in yield_ts_and_uid():
        if ts % window_size != 0:
            if window.get(uid):
                continue
            window[uid] = 1
            window_count += 1

        if ts % window_size == 0 and ts - previous_ts != 0:
            print("A minute finished:")
            print(datetime.utcfromtimestamp(ts))
            print(ts, window_count)
            print("")
            window = {}
            window_count = 0
            previous_ts = ts


def yield_ts_and_uid(json_file_path: str = "data/doodle_data.json"):
    """Simulates the stream from the topic on subscribe."""
    counter = 0
    with open(json_file_path, "r") as f:
        counter = 0
        for line in f:
            data = json.loads(line)
            yield data["ts"], data["uid"]

            counter += 1
            if counter > 100000:
                break


if __name__ == "__main__":
    main()
