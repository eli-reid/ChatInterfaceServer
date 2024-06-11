import asyncio
import websockets
import pickle
from Twitch.ChatInterface.MessageHandler import Message
from Twitch.ChatInterface import Chat as TCI
from .commandBase import commandBase
from .dataObjects import streamTimerObj

class timer(commandBase):
    def __init__(self, tci: TCI, message: Message, user, *args, **kwargs) -> None:
        self._user = user
        self.path=f"{self._user.id}/{self._user.name}/{self._user.streamTimer.token}"
        super().__init__(tci, message,'!timer')

    def start(self):
        data = pickle.dumps({"type": "timer.start", "data": None})
        self._sendBroadcast(data)

    def stop(self):
        data = pickle.dumps({"type": "timer.stop", "data": None})
        self._sendBroadcast(data)

    def addhour(self):
        currentTime = self._user.streamTimer.time
        print("addhour")
        data = pickle.dumps({"type": "timer.addhour", "data": self.data})
        self._sendBroadcast(data)
    
    def addmin(self):
        currentTime = self._user.streamTimer.time
        print("addmin")
        data = pickle.dumps({"type": "timer.addmin", "data": self.data})
        self._sendBroadcast(data)

    def _sendBroadcast(self, data:str):
        asyncio.run( self.broadcast(data, self.path))

    async def broadcast(self, data:str, path:str):
        async with websockets.connect(f"ws://localhost:8011/{path}") as ws:
            await ws.send(data)
            
    def print(self):
        pass
    
    def remove(self):
        pass
    
    def add(self):
        pass