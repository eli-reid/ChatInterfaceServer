from typing import Dict, Any
from .settings import DB
class DatabaseInterface(DB.get("TYPE")):
    def __init__(self, *args, **kwargs):
        super().__init__(**DB['SETTINGS'])
        
    def insert(self, query: tuple):
        self._execute(query)
    
    def fetchall(self, query: tuple):
        self._execute(query)
        return self._cursor.fetchall()
        
    def fetchOne(self, query: tuple):
        self._cursor = self._conn.cursor()
        self._execute(query)
        return self._cursor.fetchone()
    
    def fetchallAsDict(self, query: tuple) -> list[Dict[str, Any]]:
        return super().fetchallAsDict(query)
    
    def update(self, query: str):
        self._cursor = self._conn.cursor()
        return self._execute(query)


           

class Database:
    def __init__(self) -> None:
        self.db = DatabaseInterface()
        
    def __enter__(self) -> DatabaseInterface:
        self.db.connect()
        return self.db
    
    def __exit__(self, type, value, traceback):
        self.db.close()
        
        