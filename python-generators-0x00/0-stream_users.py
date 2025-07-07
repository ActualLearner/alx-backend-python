seed = __import__('seed')

def stream_users():
    
    try:
        connection = seed.connect_to_prodev()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data")
            for row in cursor:
                yield row
    finally:
            cursor.close()
            connection.close()
