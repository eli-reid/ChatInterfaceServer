import sqlite3
from sqlite3 import Error
from contextlib import contextmanager


class SqliteInterface:
    def __init__(self, db_file, *args, **kwargs):
        self._db_file = db_file
        self._conn = None
        self._cursor = None
        
   
    @contextmanager
    def executer(self, *args, **kwargs):
        self._connect()
        try: 
            yield self
        finally:
            self.close()
        
    
    
    def connect(self):
        try:
            self._conn = sqlite3.connect(self._db_file)
            print(f"Connected to {self._db_file}")
            self._cursor = self._conn.cursor()
        except Error as e:
            print(f"Error: {e}")
 
    def _execute(self, query, autoCommit: bool=True)-> None:
        if isinstance (query, tuple):
            sql, values = query 
            query = sql.replace("?", "{}").format(*values)
            print(f"Query: {query}")
        try:   
            self._cursor.execute(query)
            if autoCommit:
                self._conn.commit()
        except Error as e:
            print(f"Error: {e}")
    
    def close(self):
        self._conn.close()
    
        
        