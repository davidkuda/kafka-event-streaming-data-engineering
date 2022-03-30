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
                organization_name text,
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
            "INSERT INTO user_data values (?, ?, ?, ?, ?, ?)",
            (
                data["id"],
                data["username"],
                data["user_email"],
                data["user_type"],
                data["organization_name"],
                data["received_at"],
            ),
        )
        self.conn.commit()

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
        self.conn.commit()

    def delete_user(self, user_id: str):
        """Deletes a row."""
        self.cur.execute(
            f"""
            DELETE FROM user_data
            WHERE id = {user_id};
            """
        )
        self.conn.commit()


if __name__ == "__main__":
    print("hello sqlite3")
    test_db = Sqlite3Connection("manual_test.db")
    test_db.create_tables()
    org_data = """
    {
        "organization_key": "ff3959a49ac10fc70181bc00e308fbeb",
        "organization_name": "Super Mario",
        "organization_tier": "Medium",
        "created_at": "2018-01-24 17:28:09.000000"
    }
    """
    test_db.write_org_data(json.loads(org_data))
    # Here you would assert that data is in the table
    user_data_1 = """
    {
        "id": "069feb770fe581acc9d3313d59780196",
        "username": "Snake",
        "user_email": "snake@outerheaven.com",
        "user_type": "Admin",
        "organization_name": "Metal Gear Solid",
        "received_at": "2020-12-08 20:03:16.759617"
    }
    """
    test_db.create_user(json.loads(user_data_1))
    # Assert data in db
    user_data_2 = """
    {
        "id": "069feb770fe581acc9d3313d59780196",
        "username": "Snake",
        "user_email": "snake@mgs.com",
        "user_type": "Adminator",
        "organization_name": "Metal Gear Solid",
        "received_at": "2020-12-08 20:03:16.759617"
    }
    """
    d2 = json.loads(user_data_2)
    test_db.update_user(d2.get("id"), d2)

    test_db.delete_user("069feb770fe581acc9d3313d59780196")


