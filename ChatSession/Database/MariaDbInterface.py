import mariadb
import mariadb.connections
import mariadb.cursors
from mariadb import Error
from typing import Dict, List
class MariaDbInterface:
    def __init__(self, user: str, password: str, host: str, port: int, database: str,  *arg, **kwargs)-> None: 
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database   
        self._conn: mariadb.connections.Connection
        self._cursor: mariadb.cursors.Cursor

    def connect(self)-> None:  
        try:
            self._conn = mariadb.connect(        
                            user=self.user,
                            password=self.password,
                            host=self.host,
                            port=self.port,
                            database=self.database
                    )
            self._cursor = self._conn.cursor()
        except Error as e:
            print(f"Error: {e}")
    
    def _execute(self, query: tuple, autoCommit: bool=True)-> None:
        self._cursor.execute(query[0],query[1])
        if autoCommit:
            self._conn.commit()
    
    def fetchallAsDict(self, query: tuple) -> List[Dict[str, any]]:
        self._cursor = self._conn.cursor(dictionary=True)
        self._execute(query)
        return self._cursor.fetchall()       
        
    def close(self)-> None:
        self._conn.close()