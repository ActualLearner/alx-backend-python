seed = __import__('seed')

def stream_users_in_batches(batch_size):

    connection = None
    cursor = None
    try:
        connection = seed.connect_to_prodev()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data")

            while True:
                batch = cursor.fetchmany(batch_size)
                if batch == []:
                    break
                yield batch
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected:
            connection.close()

def batch_processing(batch_size):
    batch_generator = stream_users_in_batches(batch_size)
    for batch in batch_generator:
        
        for user in batch:
            if user['age'] > 25:
                print(user)
