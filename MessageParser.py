import asyncio
import pickle
from ChatSession.Settings import CHAT_SESSIONS
from ChatSession.UserChatSession import UserChatSession, User
from WebSocketServer.WebsocketServer import WebSockServer 
from html import escape as html_escape
import logging

class MessageParser:
    def __init__(self, sender: WebSockServer, data: tuple) -> None:
        self.broadcastTask: asyncio.Task
        self.sender = sender
        self.path: str = data[0]
        self.message: str = pickle.loads(data[1]) or data[1]
        if self.path not in CHAT_SESSIONS.keys():
            path_parts = self.path.split("/")
            if not path_parts[1].isnumeric():
                return
            id = int(path_parts[1])
            Name = self.cleanInput(path_parts[2])
            Key = self.cleanInput(path_parts[3])
            CHAT_SESSIONS[self.path] = UserChatSession(User(id, Name, Key))
            CHAT_SESSIONS[self.path].onLoginFail = self.logFail
        self.session: UserChatSession = CHAT_SESSIONS[self.path]
        asyncio.create_task(self.parse())
        
    def cleanInput(self, data: str) -> str:
        return html_escape(data)
        
    async def parse(self):
        await self._dispatch()
        
    async def chat_connect(self):
        logging.info("connecting Chat")
        self.session.startChatClient()
        while not self.session._twitchChat.isConnected:
            await asyncio.sleep(0.01)
        await self.chat_status()
        
    async def chat_disconnect(self):
        self.session.disconnect()
        await self.chat_status()
       
    async def chat_status(self):
        logging.info(self.sender)
        data = pickle.dumps({"type": "client.update", "data": self.session.status})
        await self.sender.broadcast(data, self.path)
 
    async def chat_load(self):
        if self.session._twitchChat.isConnected:
            self.session._user.cacheAllComands()
        
  #######################################StreamTimer Commands ############################################      
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
    def logFail(self, sender, message):
        data = pickle.dumps({"type": "client.update", "data": self.session.status})
        self.task = asyncio.create_task(self.sender.broadcast(data, self.path))
   

def getHandlerName(message: dict):
    return message.get("type","").replace(".","_")

