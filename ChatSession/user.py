from .Builtins import *
from .Database import UserDatabase
from pickle import dumps
from hashlib import sha256 as hash

class User:
    def __init__(self, id, name, key) -> None:
        self.id = id
        self.name = name
        self.key = key
        self._db = UserDatabase(self.id)
        self.commands: dict[str, commandObj] = {}
        self.quotes: list[quoteObj] = []
        self.notifications = None
        self.streamTimer: streamTimerObj 
        self.settings = self._db.loadSettings()
        

        
    def loadSettings(self):
        self.settings = self._db.loadSettings()
    
    def cacheAllComands(self):
        self.commands = self._db.loadCommands()
        self.quotes = self._db.loadQuotes()
        self.streamTimer = self._db.loadStreamTimer()
        self._commandsHash = self._getChecksum(self.commands)
        self._quotesHash = self._getChecksum(self.quotes)
        self._streamTimerHash = self._getChecksum(self.streamTimer)
        print(self._commandsHash)

    def clearCache(self):
        self.updateCommands()
        self.commands = {}
        self.quotes = []
        self.notifications = None
        
    def _getChecksum(self, data):
        return hash(dumps(data)).hexdigest()
      
    def _verifyChecksum(self, data, checksum) -> bool:
        return self._getChecksum(data) == checksum
    
    def addCommand(self, command):
        ...
        
    def updateCommands(self):
        if not self._verifyChecksum(self.commands, self._commandsHash):
            ...
        if not self._verifyChecksum(self.quotes, self._quotesHash):
            ...
        if not self._verifyChecksum(self.streamTimer, self._streamTimerHash):
            ...
