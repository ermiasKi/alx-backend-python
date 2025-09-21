import mysql.connector

def stream_users_in_batches(batch_size):
    connection = mysql.connector.connect(
            host='localhost',
            database='ALX_prodev',
            user='root',  
            password=''  
        )
    cursor = connection.cursor(buffered=False)
    cursor.execute("SELECT user_id, name, email, age FROM user_data ORDER BY user_id")
    data = cursor.fetchall()
    return data


def batch_processing(batch_size):
    batch_generator = stream_users_in_batches(batch_size)

    for batch in batch_generator:
        users_over_25 = []
        for user in batch:
            if user['age'] is not None and user['age'] > 25:
                users_over_25.append(user)
        
        yield users_over_25