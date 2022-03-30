import json
from pprint import pprint

from .sqlite3_io import Sqlite3Connection


def handle_user_events(event_data: str):

    db = Sqlite3Connection()
    d = json.loads(event_data)

    # Validation:
    if not d.get("username"):
        return
    
    # Switch:
    action = d.pop("event_type")

    if action == "User Created":
        db.create_user(d)

    elif action == "User Updated":
        d.pop("received_at")
        user_id = d.pop("id")
        db.update_user(user_id, d)

    elif action == "User Deleted":
        db.delete_user(d["id"])

    else:
        print("How to handle unrecognized event types?")


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
