import sqlite3
import functools

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Try to extract the SQL query from positional or keyword arguments
        if args:
            print(f"[LOG] Executing SQL query: {args[0]}")
        elif 'query' in kwargs:
            print(f"[LOG] Executing SQL query: {kwargs['query']}")
        else:
            print("[LOG] No SQL query found in arguments.")
        # Call the actual function
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')         # Connect to the SQLite database
    cursor = conn.cursor()                     # Create a cursor object to execute SQL commands
    cursor.execute(query)                      # Execute the passed SQL query
    results = cursor.fetchall()                # Fetch all results returned by the query
    conn.close()                               # Close the database connection
    return results                             # Return the fetched results

# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
