seed = __import__('seed')

def stream_user_ages():
    connection = None
    cursor = None
    
    try:
        connection = seed.connect_to_prodev()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute('SELECT age FROM user_data')

        for row in cursor:
            yield row['age']
        
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
        

def average_age():
    
    num = 0
    sum = 0
    for age in stream_user_ages():
        sum += age
        num += 1
    avg_age = sum/num
    print(f"Average age of users: {avg_age}")
