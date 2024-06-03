
from random import choice
from Twitch.ChatInterface.MessageHandler import Message
from Twitch.ChatInterface import Chat as TCI
from .commandBase import commandBase
from datetime import datetime, timedelta
from time import time


from .parser import CommandItem, CommandParser

class commandObj:
    def __init__(self, command:str, data:str, roleRequired:str, usage:str, cooldown:int, enabled:bool, lastUsed, user) -> None:
        self.command = command
        self.data = data
        self.roleRequired = roleRequired
        self.usage = usage
        self.cooldown = cooldown
        self.enabled = enabled
        self.lastUsed = lastUsed
        self.user = user

class command(commandBase):

    def __init__(self, tci: TCI, message: Message, user) -> None:
        self._user = user
        self._commandObj = None
        self._commandObjects: dict = self._user.commands
        super().__init__(tci, message, "!command")
        self._parser = CommandParser()

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
                command: CommandItem = self._parser.parseNewCommand(tmp)
                cmdobj = self._commandObj(command=command.command, data=command.data, roleRequired=command.roleRequired, usage=command.usage, cooldown=command.cooldown, enabled=command.enabled, user=command.user)
                cmdobj.full_clean()  
                cmdobj.save()   
                self.tci.sendMessage(self.message.channel,"Command Added")
                
    def createCommandObject(self, cmdParts):
        command: CommandItem = self._parser.parseNewCommand(cmdParts)
    def remove(self) -> None:
        pass

    def run(self, cmd:str ):
        print(f"User Role: {self.message.tags.get('mod')}")
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
    
    def _getCommandObject(self, command: str):
        return self._commandObjects.filter(command=command)