seed = __import__('seed')


def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_paginate(page_size):

    current_page = 0
    offset = current_page * page_size
    while True:
        page = paginate_users(page_size, offset)
        if page == []:
            break
        yield page
        current_page += 1
        offset = current_page * page_size
        
