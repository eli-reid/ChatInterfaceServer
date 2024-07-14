from datetime import datetime
from ..Database.DatabaseInterface import Database
from .dataObjects import quoteObj, streamTimerObj, commandObj, UserSettings
from pickle import dumps, loads


class UserDatabase:
    
    def __init__(self, id) -> None:
        self.database = Database                                                                                                                                                    
        self.id = id
        
            
    def loadCommands(self) -> dict[str, commandObj]:
        sql: tuple = "SELECT * FROM Commands_commands WHERE user_id=?",(self.id,)
        with self.database() as db:
            data = db.fetchallAsDict(sql)
        return {
            item['command']: commandObj(
                data=item['data'],
                roleRequired=item['roleRequired'],
                usage=item['usage'],
                cooldown=item['cooldown'],
                enabled=item['enabled'],
                lastUsed=item['lastUsed'],
                user=item['user_id'],
                command=item['command']
            )
            for item in data
        }
        
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
        

    def loadSettings(self) -> UserSettings:
            sql = "SELECT * FROM Chat_chatsettings WHERE user_id=?",(self.id,)
            with self.database() as db:
                data = db.fetchOne(sql)
            return UserSettings(botOAuth=data[1], botUser=data[2], streamer=data[3], streamOAuth=data[4])
    
    def loadStreamTimer(self) -> streamTimerObj:
        sql = "SELECT * FROM StreamTimer_streamtimersettings WHERE user_id=?",(self.id,)
        with self.database() as db:
            data = db.fetchOne(sql)
        return streamTimerObj(data[1], data[2], data[3], data[4])

    def updateCommands(self):
        sql = "INSERT INTO Commands_commands(user_id, command, data, cooldown, roleRequired, usage, enabled, lastUsed) VALUES (?,'?','?',?,'?','?',?,'?')"
        existingCommands = self._loadCommands()
        with self.database as db:
            for command in self.commands:
                if command not in existingCommands.keys():
                    sql = sql, (
                        self.id,
                        command,
                        self.commands[command].data,
                        self.commands[command].cooldown,
                        self.commands[command].roleRequired,
                        self.commands[command].usage,
                        self.commands[command].enabled,
                        self.commands[command].lastUsed,
                    )
                db._execute(sql)
                
    def updateCommandLastUsed(self, cmd):
        sql = "UPDATE Commands_commands SET lastUsed='?' WHERE user_id=? AND command='?'",(str(datetime.now()), self.id, cmd)
        with self.database() as db:
            db.update(sql)