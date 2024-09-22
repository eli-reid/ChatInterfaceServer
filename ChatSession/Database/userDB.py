from datetime import datetime
from .DatabaseInterface import Database
from .SqlStatments import COMMANDS_SQL, SETTINGS_SQL
from ChatSession.Builtins.dataObjects import * 
from typing import Dict



class UserDatabase: 
    def __init__(self, id: int) -> None:
        self.database = Database                                                                                                                                        
        self.id: int = id
        
    def loadSettings(self) -> UserSettings:
            with self.database() as db:
                data = db.fetchOne((SETTINGS_SQL.GET,(self.id,)))
            return UserSettings(botOAuth=data[1], botUser=data[2], streamer=data[3], streamOAuth=data[4])

    def loadCommands(self) -> Dict[str, commandObj]:
        with self.database() as db:
            data = db.fetchallAsDict((COMMANDS_SQL.SELLECT_ALL_BY_USER_ID,(self.id,)))
        return {
            item['command']: commandObj(
                id=item['id'],
                data=item['data'],
                roleRequired=item['roleRequired'],
                usage=item['usage'],
                cooldown=item['cooldown'],
                enabled=item['enabled'],
                lastUsed=item['lastUsed'],
                user_id=item['user_id'],
                command=item['command']
            )
            for item in data
        }
        
    def updateCommand(self, command: commandObj):
        statment: str = f"UPDATE Commands_commands(command, data, cooldown, \
                roleRequired, usage, enabled, lastUsed) VALUES ('?','?',?,'?','?',?,'?') \
                    WHERE user_id=? AND id=?"
       
        with self.database() as db:
                sql = statment, (     
                    command.command,
                    command.data,
                    command.cooldown,
                    command.roleRequired,
                    command.usage,
                    command.enabled,
                    command.lastUsed,
                    self.id,
                    command.id
                )
                db._execute(sql)
        
    def addCommand(self, command, data, cooldown, roleRequired, usage, enabled):
        statement = f"INPUT INTO Commands_commands(command, user_id, data, cooldown, roleRquired, usage, enabled)\
            VALUES ('?', ?, '?', '?', '?','?','?')"
        with self.database() as db:
            sql = statement, (command, self.id, data, cooldown, roleRequired, usage, enabled )
            db.insert(sql)


    def loadQuotes(self) -> dict[str, quoteObj]:
        sql = "SELECT * FROM Quotes_quotes WHERE user_id=?",(self.id,)
        with self.database() as db:
            data = db.fetchallAsDict(sql)
        return {
            item['id']: quoteObj(
                id=item['id'],
                quote=item['quote'],
                created=item['created'],
            )
            for item in data
        }
        
   
    def loadStreamTimer(self) -> streamTimerObj:
        sql = "SELECT * FROM StreamTimer_streamtimersettings WHERE user_id=?",(self.id,)
        with self.database() as db:
            data = db.fetchOne(sql)
        return streamTimerObj(data[1], data[2], data[3], data[4])

        
    def updateCommandLastUsed(self, cmd):
        sql = "UPDATE Commands_commands SET lastUsed='?' WHERE user_id=? AND command='?'",(str(datetime.now()), self.id, cmd)
        with self.database() as db:
            db.update(sql)