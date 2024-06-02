import asyncio
import pickle
from Settings import CHAT_SESSIONS
from UserChatSession import UserChatSession, User
from WebSocketServer.WebsocketServer import WebSockServer 

class MessageParser:
    def __init__(self, sender: WebSockServer, data: tuple) -> None:
        self.sender = sender
        self.messageTypes = {
            "ChatStatus": self.chatStatus,
            "ChatDisconnect": self.chatDisconnect,
            "ChatConnect": self.chatConnect,
            "ChatSettingsChange": self.chatSettingsChange,
        }
        self.path: str = data[0]
        self.message = pickle.loads(data[1]) or data[1]
        path_parts = self.path.split("/")
        self.session = CHAT_SESSIONS.get(self.path, UserChatSession(User(path_parts[1], path_parts[2], path_parts[3])))
        self.session.onLoginFail = self._onLoginFail
        self.session.onError = self._onErr
        asyncio.create_task(self.parse())
        
    async def parse(self):    
        await self.messageTypes.get(self.message.get("type"))()

    async def chatConnect(self):
        CHAT_SESSIONS.setdefault(self.path, self.session)
        self.session.startChatClient()
        await self.chatStatus()
        
    async def chatDisconnect(self):
        self.session.disconnect()
        await self.chatStatus()
        CHAT_SESSIONS.pop(self.path, None)
        
    async def chatStatus(self):
        data = pickle.dumps({"type": "ChatStatus", "data": self.session.status})
        await self.sender.broadcast(data, self.path)
 
    async def chatSettingsChange(self):
        return self.message
        
    ####################################### UserChatSession EVENT HANDLERS ############################################

    async def _onLoginFail(self, sender, message):
        await self.chatStatus()
    
    async def _onErr(self, sender, message):
        await self.chatStatus()
