import mysql.connector

def paginate_users(page_size, offset):
    connection = mysql.connector.connect(
            host='localhost',
            database='ALX_prodev',
            user='root',  
            password=''  
        )
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_paginate(page_size):
    data = paginate_users(page_size,0)

    for d in data:
        yield d

