import mariadb
from mariadb import Error
from contextlib import contextmanager


class MariaDbInterface:
    def __init__(self, user: str, password: str, host: str, port: int, database: str,  *arg, **kwargs)-> None:
            
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database   
        self._con = None
        self._cursor = None


    def connect(self)-> None:
          
        try:
            self._con = mariadb.connect(        
                            user=self.user,
                            password=self.password,
                            host=self.host,
                            port=self.port,
                            database=self.database   
                    )
            self._cursor = self._con.cursor()
        except Error as e:
            print(f"Error: {e}")
    
    def _execute(self, query: str, autoCommit: bool=True)-> None:
        self._cursor.execute(query)
        if autoCommit:
            self._con.commit()
        
    def close(self)-> None:
        self._con.close()