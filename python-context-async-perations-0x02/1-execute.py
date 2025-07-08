import mysql.connector
import os

class ExecuteQuery():
    
    def __init__(self, query, params=()):
        self.conn = None
        self.cursor = None
        self.query = query
        self.params = params
        self.DB_CONFIG = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'your_mysql_user'),
            'password': os.getenv('DB_PASS', 'your_mysql_password')
        }

    def __enter__(self):
        
        try:
            self.conn = mysql.connector.connect(**self.DB_CONFIG)
            self.cursor = self.conn.cursor(dictionary=True)
            self.cursor.execute(self.query, self.params)
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error occured: {e}")
            return []
            
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            print(f"Exeption occured on closing: {e}")
        return False
    
with ExecuteQuery('SELECT * FROM users WHERE age > %s', (25)) as eq:
    for row in eq:
        print(row)
