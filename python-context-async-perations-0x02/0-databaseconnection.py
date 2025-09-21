import sqlite3

class DatabaseConnection:
    def __init__(self, db_name='users.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()
        return False  # Don't suppress exceptions

# Usage
with DatabaseConnection() as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print("All users:")
    for row in results:
        print(row)