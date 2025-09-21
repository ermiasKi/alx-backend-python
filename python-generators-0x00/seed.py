import mysql.connector
import pandas

def connect_db():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='****'
    )
    return connection

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")

def connect_to_prodev():
    connection = mysql.connector.connect(
        host='localhost',
        database='ALX_prodev',
        user='root',
        password='****'
    )
    return connection

def create_table(connection):
    cursor = connection.cursor()
    query = """CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5,2) NOT NULL,
            INDEX user_id_index (user_id)
    )"""
    cursor.execute(query)

def insert_data(connection,data):
    df = pandas.read_csv("user_data.csv")

    cursor = connection.cursor()
    query = """INSERT INTO user_data(name,email,age)
                VALUES(%s,%s,%s)"""
    
    for row in df:
        cursor.execute(query,row['name'],row['email'],row['age'])