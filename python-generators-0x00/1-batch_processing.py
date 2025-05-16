import mysql.connector
from decimal import Decimal

def stream_users_in_batches(batch_size):
    """Yields users from the database in batches of `batch_size`"""
    # Connect to DB
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Habakkuk",
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)

    # Execute query
    cursor.execute("SELECT * FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        # Convert Decimal ages to int
        for row in batch:
            if isinstance(row['age'], Decimal):
                row['age'] = int(row['age'])
        yield batch

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """Processes batches and filters users over age 25"""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)

