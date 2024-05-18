import datetime
import sqlite3

from database.model.user import User


class DatabaseHelper:
    def __init__(self, db_path):
        self.db_path = db_path
        self.create_table('users',
                          'user_id INTEGER PRIMARY KEY, login TEXT UNIQUE, name TEXT, email TEXT, password TEXT, '
                          'logged_in INT')
        self.create_table('cookies', 'expiry_days TEXT, cookie_key TEXT, name TEXT')
        self.create_table('notes',
                          'note_id INTEGER PRIMARY KEY, login TEXT, date TEXT, note TEXT, FOREIGN KEY(login) '
                          'REFERENCES users(login)')
        self.create_table('tsp_activities',
                          'activity_id INTEGER PRIMARY KEY, login TEXT, mode TEXT, username TEXT, distance FLOAT, '
                          'permutation TEXT, ga_params TEXT,'
                          'FOREIGN KEY(login) REFERENCES users(login)')
        # If the config is empty -> insert default values
        if not (self.execute_query('SELECT count(*) FROM (select 0 from cookies limit 1)').fetchall()[0][0]):
            query = "INSERT INTO cookies (expiry_days, cookie_key, name) VALUES (?, ?, ?)"
            params = (30, 'FunGA_key', 'FunGA_cookie')
            self.execute_query(query, params)

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

    def add_user(self, user):
        query = """
            INSERT INTO users (login, name, email, password) 
            VALUES (?, ?, ?, ?)
        """
        params = (user.login, user.name, user.email, user.password)
        self.execute_query(query, params)

    def update_user(self, user):
        """Updates an existing user in the database.

        Args:
            user (User): The User object containing the updated information.
        """

        query = """
            UPDATE users
            SET name = ?, email = ?, password = ?
            WHERE login = ?
        """
        params = (user.name, user.email, user.password, user.login)
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

    def get_cookie_config(self):
        query = "SELECT expiry_days, cookie_key, name FROM cookies"
        results = self.fetchall(query)
        # Converting results to streamlit_authenticator compatible format
        config = {}  # Start with empty 'usernames' dictionary
        for (expiry_days, cookie_key, name) in results:
            config = {  # Add each user dynamically
                'name': name,
                'cookie_key': cookie_key,
                'expiry_days': expiry_days
            }
        return config

    # Exporting streamlit_authenticator credentials to SQLite
    def safe_credentials_to_database(self, yaml_credentials):
        for username, user_data in yaml_credentials['usernames'].items():
            user_exists = self.get_user_by_login(username)
            if not user_exists:  # Only insert if the user doesn't exist
                login = username
                name = user_data['name']
                email = user_data['email']
                password = user_data['password']

                self.add_user(User(login, name, email, password))

    # TODO: separate name/mail update from password update
    def update_credentials_in_database(self, yaml_credentials, active_username):
        for username, user_data in yaml_credentials['usernames'].items():
            if username == active_username:  # Only update logged-in user
                login = username
                name = user_data['name']
                email = user_data['email']
                password = user_data['password']
                self.update_user(User(login, name, email, password))

    def add_tsp_activity(self, activity):
        query = """
            INSERT INTO tsp_activities (login, mode, username, distance, permutation, ga_params) 
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            activity.login, activity.mode, activity.username, activity.distance, activity.permutation,
            activity.ga_params)
        self.execute_query(query, params)

    def get_all_tsp_activities(self):
        query = "SELECT login, mode, username, distance, permutation, ga_params FROM tsp_activities"
        return self.fetchall(query)

    def get_user_tsp_activities(self, login):
        query = "SELECT mode, distance, permutation, ga_params FROM tsp_activities WHERE login=?"
        result = self.fetchall(query, (login,))
        return result

    def get_user_tsp_activities_count_cities(self, login):
        query = "SELECT mode, distance, ga_params FROM tsp_activities WHERE login=?"
        result = self.fetchall(query, (login,))
        return result

    def get_best_tsp_activities(self, num_tsp_activities):
        query = ("SELECT mode, username, distance, permutation, ga_params FROM tsp_activities ORDER BY distance ASC "
                 "LIMIT ?")
        return self.fetchall(query, (num_tsp_activities,))


    def get_user_manual_tsp(self, login):
        query = "SELECT distance, permutation FROM tsp_activities WHERE login=? and mode=?"
        result = self.fetchall(query, (login, 'user'))
        return result

    def get_user_manual_tsp_by_city_count(self, login, city_count):
        query = (
            "SELECT distance, permutation FROM tsp_activities WHERE login=? AND mode=?")
        results = self.fetchall(query, (login, 'user'))
        difficulty_results = []
        for result in results:
            # the number of commas + 1 is the number of cities in permutation
            if result[1].count(',') + 1 == city_count:
                difficulty_results.append(result)
        return difficulty_results

    def add_note(self, active_username, note):
        query = """
            INSERT INTO notes (login, date, note) 
            VALUES (?, ?, ?)
        """
        params = (active_username, datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'), note)
        self.execute_query(query, params)

    def delete_notes(self, active_username, notes):
        """Deletes notes based on active username and a list of notes.

            Args:
            active_username (str): active username.
            notes (list[str]): A list of notes to delete.

            Warning:
                This function will delete noted based on their content (will also delete duplicated notes).
        """
        for note in notes.values:
            query = """
                    DELETE FROM notes WHERE login=? and note=?
                """
            params = (active_username, note)
            self.execute_query(query, params)

    def get_user_notes(self):
        query = "SELECT date, note FROM notes"
        return self.fetchall(query)

    def execute_query(self, query, params=None):
        """Executes a query against the database, optionally using parameters.

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): A tuple of parameters to bind to the query.

        Returns:
            The result of the query execution.
        """

        with self.connect() as conn:  # Open a database connection, "with" statement ensure automatic closure
            cursor = conn.cursor()  # Create a cursor object for query execution

            if params:
                result = cursor.execute(query, params)  # Execute with parameters
            else:
                result = cursor.execute(query)  # Execute without parameters

            conn.commit()  # Commit changes to the database
            return result

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
