from abc import ABC, abstractmethod
from Twitch.ChatInterface.MessageHandler import Message
from Twitch.ChatInterface import Chat as TCI
class CommandClass(type):
    pass
class commandBase(ABC):
    def __init__(self, tci:TCI, message: Message, cmd:str) -> None:
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

    @abstractmethod
    def add(self):
        pass
    
    @abstractmethod
    def remove(self):
        pass
    
    @abstractmethod
    def print(self):
        pass