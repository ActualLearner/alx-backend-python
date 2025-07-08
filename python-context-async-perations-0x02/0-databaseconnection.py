import mysql.connector
import os

DB_USER = os.getenv('DB_USER', 'your_mysql_user')
DB_PASS = os.getenv('DB_PASS', 'your_mysql_password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = 'ALX_prodev'

class DatabaseConnection():

    def __init__(self):
        self.conn = None
        self.DB_CONFIG = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'your_mysql_user'),
            'password': os.getenv('DB_PASS', 'your_mysql_password')
        }

    def __enter__(self):
        
        try:
            self.conn = mysql.connector.connect(**self.DB_CONFIG)
            return self.conn
        except mysql.connector.Error as e:
            print(f"Error connecting to Database: {e}")
            raise
            
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.conn.close()
        except Exception as e:
            print(f"Exeption occured on closing: {e}")
        return False
