import time
import sqlite3 
import functools

#### paste your with_db_decorator here

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        user = func(conn, *args, **kwargs)
        conn.close()
        return user


def retry_on_failure(retries, delay):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            users = None
            for r in range(retries):
                try:
                    users = func(*args, **kwargs)
                    return users
                except Exception as e:
                    time.sleep(delay)
                    if r == retries - 1:
                        print(f"Exception occured: {e}")
                        raise
                

@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)
