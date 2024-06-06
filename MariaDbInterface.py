import mariadb

class MariaDbInterface:
    def __init__(self)-> None:
        self._con = None
        self._cursor = None

    
    def _connect(self)-> None:
        self._con = mariadb.connect()
        self._cursor = self._con.cursor()
    
    def excute(self, query)-> None:
        pass
    
    def fetch(self, query)-> None:
        pass
    
    def close(self)-> None:
        pass