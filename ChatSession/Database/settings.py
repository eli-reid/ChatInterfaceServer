from .MariaDbInterface import MariaDbInterface
from .SqliteInterface import SqliteInterface




SQLITE = {
    'TYPE' : SqliteInterface,
    'SETTINGS' : {
        'db_file':'D:\\FoxZBot2\\Fox_Z_Bot\\db.sqlite3'
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