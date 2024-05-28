import sqlite3
from sqlite3 import Error

class DatabaseInterface:
    def __init__(self, db_file: str):
        self._db_file = db_file
        self._conn = None
        self._cursor = None
        self._connect()
        
    def _connect(self):
        try:
            self._conn = sqlite3.connect(self._db_file)
            self._cursor = self._conn.cursor()
        except Error as e:
            print(f"Error: {e}")
            
    def execute(self, query: str):
        self._cursor.execute(query)
        self._conn.commit()
        
    def fetch(self, query: str):
        self._cursor.execute(query)
        return self._cursor.fetchall()
    
    def close(self):
        self._conn.close()
        
    def __del__(self):
        self.close()