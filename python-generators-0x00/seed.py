import mysql.connector
import csv
import os
from uuid import uuid4

# --- IMPORTANT ---
# Before running, make sure to set your MySQL credentials as environment variables
# or replace the os.getenv calls with your actual username and password.
DB_USER = os.getenv('DB_USER', 'your_mysql_user')
DB_PASS = os.getenv('DB_PASS', 'your_mysql_password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = 'ALX_prodev'


def connect_db():
    """
    Connects to the MySQL database server.
    Does NOT connect to a specific database initially.
    """
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """Creates the database ALX_prodev if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        # print(f"Database '{DB_NAME}' created or already exists.")
    except mysql.connector.Error as e:
        print(f"Failed to create database: {e}")
    finally:
        cursor.close()


def connect_to_prodev():
    """Connects to the ALX_prodev database in MYSQL."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to database '{DB_NAME}': {e}")
        return None


def create_table(connection):
    """Creates a table user_data if it does not exist with the required fields."""
    cursor = connection.cursor()
    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age INT NOT NULL,
            INDEX(user_id)
        );
        """
        cursor.execute(create_table_query)
        print("Table user_data created successfully")
    except mysql.connector.Error as e:
        print(f"Failed to create table: {e}")
    finally:
        cursor.close()


def insert_data(connection, csv_file_path):
    """Inserts data from a CSV file into the database if it does not exist."""
    cursor = connection.cursor()
    
    # Check if the table is empty before inserting
    cursor.execute("SELECT COUNT(*) FROM user_data")
    if cursor.fetchone()[0] > 0:
        # print("Data already exists in user_data. Skipping insertion.")
        return

    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Assuming the CSV has columns 'name', 'email', 'age'
                # The user_id will be generated.
                insert_query = """
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                """
                # Generate a new UUID for each user
                user_id = str(uuid4())
                user_data = (user_id, row['name'], row['email'], int(float(row['age'])))
                cursor.execute(insert_query, user_data)
        
        connection.commit()
        # print(f"Data from {csv_file_path} inserted successfully.")
    except FileNotFoundError:
        print(f"Error: The file {csv_file_path} was not found.")
    except mysql.connector.Error as e:
        print(f"Failed to insert data: {e}")
        connection.rollback() # Rollback changes on error
    finally:
        cursor.close()
