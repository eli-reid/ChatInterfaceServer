from django.apps import apps
from django.db.models import Model, QuerySet
from random import choice
from Twitch.ChatInterface.MessageHandler import Message
from Twitch.ChatInterface import Chat as TCI
from .commandBase import commandBase


class userCommand():

    def __init__(self, tci: TCI, message: Message, command: str ) -> None:
        self.tci = tci
        self.message = message
        self.command: str = command
        self._commandObj: Model = apps.get_model("Commands","Command")
        self._commandlist: list = list(self.commandObj.objects.all().values_list('command', flat=True))
        self._command: QuerySet = self._commandObj.objects.filter(command=command)
        commandMsgSplit = self.message.text.split()
        self.params = {
            "$userid" : self.message.username.lower(),
            "$username" : self.message.username,
            "$targetid": commandMsgSplit[commandMsgSplit.index(self.command)].lower(),
            "$randuserid": self.tci.channels[self.message.channel]
        }       
        
        if self._command.count():
            self._parseCommand()


    def print(self) -> None:

        self.tci.sendMessage(self.message.channel,"command worked")

    def _parseCommand(self) -> None:
        cmd: str = self._command["command"]
        for key,value in self.params:
            cmd.replace(key,value)
            
        
