from .MariaDbInterface import MariaDbInterface
from .SqliteInterface import SqliteInterface




SQLITE = {
    'TYPE' : SqliteInterface,
    'SETTINGS' : {
        'db_file':'/home/django/fox.db'
        }
}

MARIADB = {
    'TYPE' : MariaDbInterface,
    'SETTINGS' : {
        'user' : None,
        'Password' : None,
        'host' : None,
        'port' : None,
        'database' : None
    }
}

DB = SQLITE