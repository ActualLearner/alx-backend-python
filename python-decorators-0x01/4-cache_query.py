import time
import sqlite3 
import functools


query_cache = {}

"""your code goes here"""

def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs['query']
        if query in query_cache:
            return query_cache[query]
        users = func(*args, **kwargs)
        query_cache[query] = users
        return query_cache[query]

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
