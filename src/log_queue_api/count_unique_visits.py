from pprint import pprint
from datetime import datetime
import json

from .json_io import yield_ts_and_uid


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
    for ts, uid in yield_ts_and_uid(limit=10000):
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


if __name__ == "__main__":
    main()
