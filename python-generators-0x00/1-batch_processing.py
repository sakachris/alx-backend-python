import mysql.connector
from decimal import Decimal

def stream_users_in_batches(batch_size):
    """Yields batches of users from the database"""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Habakkuk",
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        for user in batch:
            if isinstance(user['age'], Decimal):
                user['age'] = int(user['age'])
        yield batch

    cursor.close()
    connection.close()
    return

def batch_processing(batch_size):
    """Prints users over age 25 from each batch"""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
    return
