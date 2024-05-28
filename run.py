from WebSocketServer.WebsocketServer import WebSockServer as WS
from UserChatSession import UserChatSession
from typing import Dict, Any
import asyncio
import redis
import pickle

def onChatStatus(sender, data):
    pass

def onChatConnect(sender, data):
    pass

def onchatDisconnect(sender, data):
    pass

def onMsg(sender: WS, message: Dict[str, Any]):
    print(message)
    if message.get("type") == "NewConnection":
        print(f"New Connection from {message.get('data')}")
        data = pickle.dumps(message.get('data'))
        asyncio.create_task(sender.broadcast(data, message.get('websocket').path))
  


def onstreamtimer(sender, data):
    pass

server = WS()
loop = asyncio.new_event_loop()


server.event.on('message', onMsg)
loop.run_until_complete(server.start())


