import sqlite3


class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name  # Database file name
        self.query = query  # SQL query string
        self.params = params or ()  # Parameters for the query
        self.connection = None  # Will hold the database connection
        self.cursor = None  # Will hold the cursor object
        self.result = None  # Will hold the result of the query

    def __enter__(self):
        # Open connection and execute the query
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result  # Return the result of the query

    def __exit__(self, exc_type, exc_value, traceback):
        # Close connection safely
        if self.connection:
            self.connection.commit()
            self.connection.close()
        if exc_type:
            print(f"An error occurred: {exc_value}")
        return False  # Propagate any exceptions


# --------- Setup database for demonstration ---------
def setup_demo_data():
    with sqlite3.connect("example.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        """
        )
        cursor.executemany(
            "INSERT INTO users (name, age) VALUES (?, ?)",
            [("Alice", 22), ("Bob", 30), ("Charlie", 27), ("Diana", 19), ("Eve", 35)],
        )
        conn.commit()


setup_demo_data()

# --------- Use the ExecuteQuery context manager ---------
query = "SELECT * FROM users WHERE age > ?"
param = (25,)

with ExecuteQuery("example.db", query, param) as results:
    for row in results:
        print(row)
