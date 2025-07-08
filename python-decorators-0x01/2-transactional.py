import sqlite3 
import functools


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        user = func(conn, *args, **kwargs)
        conn.close()
        return user

def transactional(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        
        try:
            func(*args, **kwargs)
            conn = args[0]
            conn.commit()
        except Exception as e:
            print(f"An error occured {e}. Rolling back...")
            conn.rollback()
            
        

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
    #### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
