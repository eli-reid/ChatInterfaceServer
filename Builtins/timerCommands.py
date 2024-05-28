from threading import Thread
from django.apps import apps
from django.db.models import Model
from random import choice
from Twitch.ChatInterface.MessageHandler import Message
from Twitch.ChatInterface import Chat as TCI
from .commandBase import commandBase
import asyncio

class timer(commandBase):

    def __init__(self, tci: TCI, message: Message) -> None:
        Websock = apps.get_app_config("Websock")
        #websocket address path 
        self.path = "/"
        self.broadcast = Websock.broadcast
        super().__init__(tci, message,'!timer')
        

    def add(self):
        return

    def remove(self):
        return
    
    def start(self):
        return

    def stop(self):
        self._sendBroadcast('{"event":"EVENT_STOP","data": " "}')

    def addhour(self):
        return 

    def print(self):
        return

    def _sendBroadcast(self, data:str):
            asyncio.run( self.broadcast(data, self.path))
