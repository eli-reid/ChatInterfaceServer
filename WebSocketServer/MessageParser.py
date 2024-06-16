import asyncio
import pickle
from ChatSession.Settings import CHAT_SESSIONS
from ChatSession.UserChatSession import UserChatSession, User
from .WebsocketServer import WebSockServer 

class MessageParser:
    def __init__(self, sender: WebSockServer, data: tuple) -> None:
        self.sender = sender
        self.path: str = data[0]
        self.message = pickle.loads(data[1]) or data[1]
        if self.path not in CHAT_SESSIONS:
            path_parts = self.path.split("/")
            CHAT_SESSIONS[self.path] = UserChatSession(User(path_parts[1], path_parts[2], path_parts[3]))
        self.session: UserChatSession = CHAT_SESSIONS[self.path]
        self.session.onLoginFail = self._onLoginFail
        self.session.onError = self._onErr
        asyncio.create_task(self.parse())
        
    async def parse(self):
        print(f"PARSING: {self.message}")
        await self._dispatch()
        
    async def chat_connect(self):
        self.session.startChatClient()
        while not self.session._twitchChat.isConnected:
            await asyncio.sleep(0.5)
        await self.chat_status()
        
    async def chat_disconnect(self):
        self.session.disconnect()
        await self.chat_status()
       
    async def chat_status(self):
        data = pickle.dumps({"type": "client.update", "data": self.session.status})
        await self.sender.broadcast(data, self.path)
 
    async def chat_load(self):
        self.session._user.loadSettings()
        
    async def timer_update(self):
        await self.sender.broadcast(pickle.dumps(self.message), self.path)
    
    async def timer_stop(self):
        await self.sender.broadcast(pickle.dumps(self.message), self.path)
    
    async def timer_start(self):
        await self.sender.broadcast(pickle.dumps(self.message), self.path)
    
    async def timer_addhour(self):
        await self.sender.broadcast(pickle.dumps(self.message), self.path)
    
    async def timer_addmin(self):
        await self.sender.broadcast(pickle.dumps(self.message), self.path) 
 
        
    async def _dispatch(self):
        handler = getattr(self, getHandlerName(self.message), None)
        if handler is not None:
            await handler()
        
    ####################################### UserChatSession EVENT HANDLERS ############################################

    async def _onLoginFail(self, sender, message):
        await self.chatStatus()
    
    async def _onErr(self, sender, message):
        await self.chatStatus()

def getHandlerName(message: dict):
    return message.get("type").replace(".","_")