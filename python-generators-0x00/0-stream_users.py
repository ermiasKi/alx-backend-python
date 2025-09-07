import mysql.connector


def stream_user():
    connection = mysql.connector.connect(
            host='localhost',
            database='ALX_prodev',
            user='root',
            password=''
        )
        
    cursor = connection.cursor(buffered=False)
    
    # Execute the query
    cursor.execute("SELECT user_id, name, email, age FROM user_data")
    
    # Fetch and yield rows one by one
    row = cursor.fetchone()
    while row is not None:
        yield {
            'user_id': row[0],
            'name': row[1],
            'email': row[2],
            'age': float(row[3]) if row[3] is not None else None
        }
        row = cursor.fetchone()