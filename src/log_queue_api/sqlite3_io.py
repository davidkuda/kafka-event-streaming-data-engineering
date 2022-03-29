import os
import sqlite3


DB_FILE_PATH = "data.sqlite3"


class Sqlite3Connection:
    
    def __init__(self, path: str = DB_FILE_PATH):
        self.conn = sqlite3.Connection(path)
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.close()
    
    def create_tables(self):
        """Creates the two tables organization_data and user_data."""
        self.cur.execute(
            """
            CREATE TABLE organization_data (
                organization_key text,
                organization_name text,
                organization_tier text,
                created_at text
            )
            """
        )
        self.cur.execute(
            """
            CREATE TABLE user_data (
                id text primary key,
                username text,
                user_email text,
                user_type text,
                organizational_name text
            )
            """
        )
        self.conn.commit()
        
    def remove_existing_db_file(self):
        """Removes the db file if it exists."""
        if os.path.exists(DB_FILE_PATH):
            os.remove(DB_FILE_PATH)
        return

    def write_org_data(self, data: dict):
        """Write a row of organization data to db."""
        self.cur.execute(
            "INSERT INTO organization_data values (?, ?, ?, ?)",
            (
                data["organization_key"],
                data["organization_name"],
                data["organization_tier"],
                data["created_at"],
            ),
        )
        self.conn.commit()

    def create_user(self, row_data: dict):
        """Write a row of user data to db."""
        raise NotImplementedError
    
    def update_user(self, user_name, update_data):
        raise NotImplementedError
    
    def delete_user(self, user_name):
        raise NotImplementedError


    if __name__ == "__main__":
        print("hello sqlite3")
