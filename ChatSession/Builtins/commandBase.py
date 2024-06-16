from abc import ABC, abstractmethod, abstractproperty
from Twitch_Edog0049a import ChatInterface as TCI
from Twitch_Edog0049a.ChatInterface.MessageHandler import Message



class commandBase(ABC):
    def __init__(self, tci:TCI, message: Message, cmd:str, roleRequire, cooldown=30, *args, **kwargs ) -> None:
        self._roleReqired = roleRequire
        self.message = message
        self.tci = tci
        self.data = self.message.text
        if self.message.text.split(" ")[0] == cmd:
            self.data = self.data.replace(f"{cmd} ", "")
            action = self.message.text.split(" ")[1] if len(self.message.text.split(" "))>1 else None
            if action in self.__dir__():
                self.data = self.data.replace(f"{action} ","")
                getattr(self, action)()
            else:
                print("command print")
                self.print() 
    @property
    def roleRequired(self):
        return self._roleReqired
    
    
    @abstractmethod
    def add(self):
        ...
    
    @abstractmethod
    def remove(self):
        ...
    
    @abstractmethod
    def print(self):
        ...