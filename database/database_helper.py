import sqlite3

from database.model.user import User


class DatabaseHelper:
    def __init__(self, db_path):
        self.db_path = db_path
        self.create_table('activities', 'activity_id INTEGER PRIMARY KEY, login TEXT, game TEXT, data TEXT')
        self.create_table('users',
                          'user_id INTEGER PRIMARY KEY, login TEXT, name TEXT, email TEXT, password TEXT, logged_in INT')
        # TODO: implement cookie settings from database
        self.create_table('cookies', 'expiry_days TEXT, key TEXT, name TEXT')

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

    def get_all_user_credentials(self):
        query = "SELECT login, name, email, password FROM users"
        results = self.fetchall(query)
        # Converting results to streamlit_authenticator compatible format
        credentials = {'usernames': {}}  # Start with empty 'usernames' dictionary
        for (login, name, email, password) in results:
            credentials['usernames'][login] = {  # Add each user dynamically
                'name': name,
                'email': email,
                'password': password
            }
        return credentials

    def import_users_from_yaml(self, yaml_credentials):
        for username, user_data in yaml_credentials['usernames'].items():
            user_exists = self.get_user_by_login(username)
            if not user_exists:  # Only insert if the user doesn't exist
                login = username
                name = user_data['name']
                email = user_data['email']
                password = user_data['password']

                self.add_user(User(login, name, email, password))

    def fetchall(self, query, params=None):
        """Executes a query and returns all results as a list of tuples.

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Optional parameters to bind to the query.

        Returns:
            list: A list of tuples, where each tuple represents a row of results.
        """

        with self.connect() as conn:
            cursor = conn.cursor()
            if params:
                result = cursor.execute(query, params)
            else:
                result = cursor.execute(query)
            return result.fetchall()
