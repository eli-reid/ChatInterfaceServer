from random import choice
from Twitch_Edog0049a.ChatInterface.MessageHandler import Message
from Twitch_Edog0049a.ChatInterface import Chat as TCI
from .commandBase import commandBase
from .dataObjects import quoteObj

class quote(commandBase):
    def __init__(self, tci:TCI, message: Message, user) -> None:
        super().__init__(tci, message, "!quote")
       
    def print(self):
            pass

    def add(self):
        pass
    
    def remove(self):
        pass
        