from contextlib import contextmanager
from .settings import SQLITE as DB

class DatabaseInterface(DB['TYPE']):
    def __init__(self, *args, **kwargs):
        super().__init__(**DB['SETTINGS'])
        
    def insert(self, query: str):
        self._execute(query)
    
    def fetchall(self, query: str):
        self._execute(query)
        return self._cursor.fetchall()
        
    def fetchOne(self, query: str):
        self._execute(query)
        return self._cursor.fetchone()
    
    def fetchallAsDict(self, query: str):
        self._conn.row_factory = dict_factory
        self._cursor = self._conn.cursor()
        self._execute(query)
        return self._cursor.fetchall()

def dict_factory(cursor, row):
        return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
           
        
@contextmanager       
def DBConnect(db):
    try:
        db.connect()
        yield db
    finally:
        db.close