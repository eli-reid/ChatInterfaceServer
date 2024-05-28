
from random import choice
from Twitch.ChatInterface.MessageHandler import Message
from Twitch.ChatInterface import Chat as TCI
from .commandBase import commandBase


class quote(commandBase):
    def __init__(self, tci:TCI, message: Message, user) -> None:
        self._user = user
        self._quotesObj = self._user.quotes.all()
        self._ids = list(self._quotesObj.values_list('pk',flat=True))
        super().__init__(tci, message, "!quote")
       
    def print(self):
        print(self._ids)
        try:
            if self.data is not None and self.data.isnumeric() and int(self.data) in self._ids:
                quoteobj = self._quotesObj.get(id=self.data)
            else:
                quoteobj = self._quotesObj.get(id=choice(self._ids))
            self.tci.sendMessage(self.message.channel,f"id: {quoteobj.id}, { quoteobj.quote}")
        except:
            pass

    def add(self):
        if self.data is not None and self._quotesObj.filter(quote=self.data).count() > 0:
            self.tci.sendMessage(self.message.channel,f"{self.data} has already been added!")
        else:
            newQuote = Quotes()
            newQuote.quote = self.data
            newQuote.user = self._user
            newQuote.full_clean()
            newQuote.save()
            self.tci.sendMessage(self.message.channel,"quote added")
    
    def remove(self):
        if self.data is not None and self.data.isnumeric() and int(self.data) in self._ids:
            self._quotesObj.get(id=self.data).delete()
            self.tci.sendMessage(self.message.channel, f"Quote {self.data} Removed!")
        