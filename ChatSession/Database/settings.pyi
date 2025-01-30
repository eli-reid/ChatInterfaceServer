from typing import TypedDict

class DbSetting(TypedDict):
    NAME: str
    TYPE: object
    SETTINGS: dict

SQLITE: DbSetting
MARIADB: DbSetting
DB: DbSetting
