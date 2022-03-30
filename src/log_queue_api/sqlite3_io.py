import os
import sqlite3


DB_FILE_PATH = "./data/data.sqlite3"


class Sqlite3Connection:
    def __init__(self, path: str = DB_FILE_PATH):
        self.conn = sqlite3.connect(path)
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
                organizational_name text,
                created_at text
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

    def create_user(self, data: dict):
        """Write a row of user data to db."""
        self.cur.execute(
            "INSERT INTO user_data VALUES (?, ?, ?, ?, ?)",
            (
                data["id"],
                data["username"],
                data["user_email"],
                data["user_type"],
                data["organization_name"],
                data["received_at"],
            ),
        )

    def update_user(self, user_id: str, update_data: str):
        """Update an existing user row."""
        self.cur.execute(
            f"""
            UPDATE user_data
            SET username = ? ,
                user_email = ? ,
                user_type = ? ,
                organization_name = ?
            WHERE
                id = {user_id};
            """,
            (
                update_data["username"],
                update_data["user_email"],
                update_data["user_type"],
                update_data["organization_name"],
            )
        )

    def delete_user(self, user_id: str):
        """Deletes a row."""
        self.cur.execute(
            f"""
            DELETE FROM user_data
            WHERE id = {user_id};
            """
        )


if __name__ == "__main__":
    print("hello sqlite3")
