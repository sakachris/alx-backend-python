import time
import sqlite3
import functools


# Decorator that opens and closes a database connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()

    return wrapper


# Decorator to retry a function if it raises an exception
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)  # Try running the function
                except Exception as e:
                    attempt += 1
                    print(f"[Retry {attempt}/{retries}] Error: {e}")
                    if attempt < retries:
                        time.sleep(delay)  # Wait before retrying
                    else:
                        print("All retries failed. Raising exception.")
                        raise  # Re-raise the last exception after all retries

        return wrapper

    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# Attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)
