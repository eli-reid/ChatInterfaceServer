from .MariaDbInterface import MariaDbInterface
from .SqliteInterface import SqliteInterface
from typing import TypedDict, Dict

class DbSetting(TypedDict):
    NAME: str
    TYPE: object
    SETTINGS: Dict


SQLITE: DbSetting = {
    'NAME': 'SQLITE',
    'TYPE' : SqliteInterface,
    'SETTINGS' : {
        'db_file':'D:\\FoxZBot2\\Fox_Z_Bot\\db.sqlite3'
        }
}

MARIADB: DbSetting = {
    'NAME': 'MARIADB',
    'TYPE' : MariaDbInterface,
    'SETTINGS' : {
        'user' : None,
        'Password' : None,
        'host' : None,
        'port' : None,
        'database' : None
    }
}

DB: DbSetting = SQLITE