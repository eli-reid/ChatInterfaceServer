import mysql.connector
import mysql.connector.django
import mysql.connector.django.client

class MySQLInterface:
    def __init__(self)-> None:
        self._con = None
        self._cursor = None

    
    def _connect(self)-> None:
        self._con =mysql.connector.connect()
        self._cursor = self._con.cursor()
    
    def excute(self, query)-> None:
        pass
    
    def fetch(self, query)-> None:
        pass
    
    def close(self)-> None:
        pass