import sqlite3


class DatabaseHelper:
    def __init__(self, db_path):
        self.db_path = db_path
        self.create_table('activities', 'activity_id INTEGER PRIMARY KEY, login TEXT, game TEXT, data TEXT')
        self.create_table('users', 'user_id INTEGER PRIMARY KEY, login TEXT, name TEXT, email TEXT, password TEXT')

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

    def add_user(self, user):
        query = """
            INSERT INTO users (login, name, email, password) 
            VALUES (?, ?, ?, ?)
        """
        params = (user.login, user.name, user.email, user.password)
        self.execute_query(query, params)

    def get_user_by_login(self, login):
        query = "SELECT * FROM users WHERE login=?"
        result = self.fetchall(query, (login,))
        return result  # Might return a list of 1 element, or empty list
