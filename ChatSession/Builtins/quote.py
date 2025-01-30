from random import choice
from Twitch_Edog0049a.ChatInterface.MessageHandler import Message
from Twitch_Edog0049a.ChatInterface import Chat as TCI
from .commandBase import commandBase
from .dataObjects import quoteObj


class quote(commandBase):
    def __init__(self, tci:TCI, message: Message, user) -> None:
        self._user = user
        self._quotesObj: dict  = self._user.quotes
        self._ids = self._quotesObj.keys()
        super().__init__(tci, message, "!quote", roleRequire=None)
       
    def print(self):
        try:
            if self.data is not None and self.data.isnumeric() and int(self.data) in self._ids:
                quoteobj = self._quotesObj.get(self.data)
            else:
                quoteobj = self._quotesObj.get(choice(self._ids))
            self.tci.sendMessage(self.message.channel,f"id: {quoteobj.id}, { quoteobj.getquote}")
        except:
            pass

    def add(self):
        if self.data is not None and self._quotesObj.objects.filter(quote=self.data).count() > 0:
            self.tci.sendMessage(self.message.channel,f"{self.data} has already been added!")
        else:
            self.tci.sendMessage(self.message.channel,"quote added")
    
    def remove(self):
        if self.data is not None and self.data.isnumeric() and int(self.data) in self._ids:
            
            self.tci.sendMessage(self.message.channel, f"Quote {self.data} Removed!")
    