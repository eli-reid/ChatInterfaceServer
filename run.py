from Settings import CHAT_SESSIONS
from WebSocketServer.WebsocketServer import WebSockServer as WS
from UserChatSession import UserChatSession
from parser_1 import MessageParser
from typing import Dict, Any
import asyncio
import redis
import pickle
from threading import Thread


server = WS(port=8011)
loop = asyncio.new_event_loop()


def run():
    try:
        
        server.event.on('message', MessageParser)
        loop.run_until_complete(server.start())
    except KeyboardInterrupt as e:
        for key, session in CHAT_SESSIONS.items():
            session.disconnect()
        loop. run_until_complete(server.stop())

run()
