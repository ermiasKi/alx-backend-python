import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=None, db_name='users.db'):
        self.query = query
        self.params = params or ()
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.results = None
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()
        return False

# Usage
with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as results:
    print("Users older than 25:")
    for row in results:
        print(row)