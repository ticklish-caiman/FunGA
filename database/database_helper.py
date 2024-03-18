import sqlite3


class DatabaseHelper:
    def __init__(self, db_path):
        self.db_path = db_path
        self.create_table('activities', 'activity_id INTEGER PRIMARY KEY, login TEXT, game TEXT, data TEXT')

    def create_table(self, table_name, table_schema):
        """Creates a table if it doesn't exist.

        Args:
            table_name (str): The name of the table to create.
            table_schema (str): The SQL schema for the table (columns and data types).
        """
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({table_schema})"
        self.execute_query(query)

    def connect(self):
        return sqlite3.connect(self.db_path)

    def execute_query(self, query, params=None):
        with self.connect() as conn:
            cursor = conn.cursor()

            if params:
                result = cursor.execute(query, params)
            else:
                result = cursor.execute(query)
            conn.commit()
            return result
