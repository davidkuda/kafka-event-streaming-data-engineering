import json
from pprint import pprint

from .sqlite3_io import Sqlite3Connection


def handle_user_events(event_data: str):
    print("Handling user Event:")
    pprint(event_data)


def handle_org_events(data: str):
        """Load new org event messages to database.
        
        Args:
            data (str): String representation of json.
            db_conn (sqlite3.Connection): Conn to db that has method "write_org_dat
        """
        d = json.loads(data)
        db = Sqlite3Connection()
        db.write_org_data(d)
        print("Written org data to db.")
