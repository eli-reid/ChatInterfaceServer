from typing import Any
from ..Database.DatabaseInterface import DatabaseInterface, DBConnect
from .command import commandObj      
from .quote import quoteObj
from .timer import streamTimerObj


class UserSettings:
    def __init__(self,botUser=None, botOAuth=None, streamer=None, streamOAuth=None) -> None:
        self.BotUser = botUser
        self.BotOAuth = botOAuth
        self.Streamer = streamer
        self.StreamerOAuth = streamOAuth

class User:
    def __init__(self, id, name, key) -> None:
        self.id = id
        self.name = name
        self.key = key
        self._db = DatabaseInterface()
        self.commands: list[commandObj] = None
        self.quotes: list[quoteObj] = None
        self.notifications = None
        self.streamTimer: streamTimerObj = None
        self.settings = self._loadSettings()
        
        
    def _loadCommands(self) -> dict[str, commandObj]:
        sql = "SELECT * FROM Commands_commands WHERE user_id=?",(self.id,)
        with DBConnect(self._db) as db:
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
            )
            for item in data
        }
        
    def _loadQuotes(self) -> dict[str, quoteObj]:
        sql = "SELECT * FROM Quotes_quotes WHERE user_id=?",(self.id,)
        with DBConnect(self._db) as db:
            data = db.fetchallAsDict(sql)
        return {
            item['id']: quoteObj(
                id=item['id'],
                quote=item['quote'],
                created=item['created'],
            )
            for item in data
        }
        

    def _loadSettings(self) -> UserSettings:
            sql = "SELECT * FROM Chat_chatsettings WHERE user_id=?",(self.id,)
            with DBConnect(self._db) as db:
                data = db.fetchOne(sql)
            return UserSettings(botOAuth=data[1], botUser=data[2], streamer=data[3], streamOAuth=data[4])
    
    def _loadStreamTimer(self) -> Any:
        sql = "SELECT * FROM StreamTimer_streamtimersettings WHERE user_id=?",(self.id,)
        with DBConnect(self._db) as db:
            data = db.fetchOne(sql)
        return streamTimerObj(data[1], data[2], data[3], data[4])

    def loadSettings(self):
        self.settings = self._loadSettings()
    
    def cacheAllComands(self):
        self.commands = self._loadCommands()
        self.quotes = self._loadQuotes()
        self.streamTimer = self._loadStreamTimer()
    
    def clearCache(self):
        self.commands = None
        self.quotes = None
        self.notifications = None
        
        
    def updateCommands(self):
        sql = "INSERT INTO Commands_commands(user_id, command, data, cooldown, roleRequired, usage, enabled, lastUsed) VALUES (?,'?','?',?,'?','?',?,'?')"
        existingCommands = self._loadCommands()
        with DBConnect(self._db) as db:
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
      
        
        