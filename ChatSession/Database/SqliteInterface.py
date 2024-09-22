import sqlite3
from sqlite3 import Error
from typing import Dict, List
import logging
class SqliteInterface:
    def __init__(self, db_file, *args, **kwargs):
        self._db_file = db_file
        self._conn = None
        self._cursor = None
        
    def connect(self):
        try:
            self._conn = sqlite3.connect(self._db_file)
            print(f"Connected to {self._db_file}")
            self._cursor = self._conn.cursor()
        except Exception as e:
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
    
    def fetchallAsDict(self, query: tuple) -> List[Dict[str, any]]:
        self._conn.row_factory = self._dict_factory
        self._execute(query)
        return self._cursor.fetchall()
    
    def _dict_factory(cursor, row)-> Dict[any,any]:
        return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
    
    def close(self):
        try:
            self._conn.close()
        except:
            pass
    
        
        