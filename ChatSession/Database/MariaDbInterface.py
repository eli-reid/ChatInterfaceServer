import mariadb
from mariadb import Error

class MariaDbInterface:
    def __init__(self)-> None:
        self._con = None
        self._cursor = None
    
    def _connect(self, user: str, password: str, host: str, port: int, database: str)-> None:
        try:
            self._con = mariadb.connect(        
                            user=user,
                            password=password,
                            host=host,
                            port=port,
                            database=database   
                    )
            self._cursor = self._con.cursor()
        except Error as e:
            print(f"Error: {e}")
    
    def _execute(self, query: str, autoCommit: bool=True)-> None:
        self._cursor.execute(query)
        if autoCommit:
            self._con.commit()
        
    def _close(self)-> None:
        self._con.close()