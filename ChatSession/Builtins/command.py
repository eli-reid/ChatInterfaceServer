from random import choice
from Twitch_Edog0049a.ChatInterface.MessageHandler import Message
from Twitch_Edog0049a.ChatInterface import Chat as TCI
from .commandBase import commandBase
from datetime import datetime
from time import time
from .commandParser import CommandParser
from .dataObjects import commandObj


class command(commandBase):
    def __init__(self, tci: TCI, message: Message, user) -> None:
        self._user = user
        self._commandObjects: dict = self._user.commands
        self._parser = CommandParser()
        super().__init__(tci, message, "!command", roleRequire='mod')
        
    def print(self) -> None:
       self.tci.sendMessage(self.message.channel, "Command List: " + ", ".join(self.commands))
            
    def add(self) -> None:     
        if self.data is not None and self.isCommand(self.data.split(" ")[0]) :
            self.tci.sendMessage(self.message.channel,"Command already exists")
        else:
            tmp = self.data.split(" ")
            if len(tmp)<2:
                self.tci.sendMessage(self.message.channel, "command has no data")
            else:
                command: commandObj = self._parser.parseNewCommand(tmp, self._user.id)
                self._user.commands[command.command] = command
                self.tci.sendMessage(self.message.channel,"Command Added")
                
    def createCommandObject(self, cmdParts):
        command: commandObj = self._parser.parseNewCommand(cmdParts)
        
    def remove(self) -> None:
        pass

    def run(self, cmd:str ):
        if self.isCommand(cmd):
            commandObject = self._commandObjects.get(cmd)
            iscoolDown: bool = self.onCoolDown(commandObject)
            print(f"Command: {commandObject.command} Cooldown: {commandObject.cooldown} LastUsed: {commandObject.lastUsed} isCoolDown: {iscoolDown}")
            if (commandObject.lastUsed is None or commandObject.cooldown==0 or not iscoolDown) and commandObject.enabled:
                if commandObject.cooldown > 0:
                    commandObject.lastUsed = str(datetime.now())
                commandStr: str = self._parser.parseCommand(self.tci, self.message, commandObject.data)
                
                self.tci.sendMessage(self.message.channel, commandStr)


    def onCoolDown(self, commandObj) -> bool:
        lastUsed: float = datetime.timestamp(datetime.strptime(commandObj.lastUsed, "%Y-%m-%d %H:%M:%S.%f"))
        currentTime: float = datetime.timestamp(datetime.now())
        cooldown: int = commandObj.cooldown
        return currentTime - lastUsed <= cooldown
       
    @property
    def commands(self)->list:
        return self._commandObjects.keys()

    def isCommand(self, command: str)->bool:
        return command in self._commandObjects.keys() or command in globals()
    
    def _getCommandObject(self, command: str) -> commandObj:
        return self._commandObjects.get(command)