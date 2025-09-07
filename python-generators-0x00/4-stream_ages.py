import mysql.connector


def stream_user_ages():
    connection = mysql.connector.connect(
            host='localhost',
            database='ALX_prodev',
            user='root',  
            password=''  
        )
    
    cursor = connection.cursor()

    data = cursor.execute("SELECT age FROM user_data")

    for d in data:
        yield d
        

def average():
    total = 0
    count = 0
    data = stream_user_ages()
    for i in data:
        total += i
        count += 1
    
    averag = total//count
    print(f"Average age of users: {averag}")