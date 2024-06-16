from .SqliteInterface import SqliteInterface
#from .MariaDbInterface import MariaDbInterface


class DatabaseInterface(SqliteInterface):
    def __init__(self):
        super().__init__("F:\\FoxZBot2\\Fox_Z_Bot\\db.sqlite3")
        
    def insert(self, query: str):
        self._execute(query)
    
    def fetchall(self, query: str):
        self._execute(query)
        return self._cursor.fetchall()
        
    def fetchOne(self, query: str):
        self._execute(query)
        return self._cursor.fetchone()
    
    def fetchallAsDict(self, query: str):
        self._conn.row_factory = self.dict_factory
        self._cursor = self._conn.cursor()
        self._execute(query)
        return self._cursor.fetchall()
    
    def dict_factory(self, cursor, row):
        return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
        