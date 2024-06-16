from ChatSession.Settings import CHAT_SESSIONS
from WebSocketServer.WebsocketServer import WebSockServer as WS
from WebSocketServer.MessageParser import MessageParser
import asyncio

def run():
    try:
        server = WS(port=8011)
        loop = asyncio.new_event_loop()
        server.event.on('message', MessageParser)
        loop.run_until_complete(server.start())
    except KeyboardInterrupt as e:
        for key, session in CHAT_SESSIONS.items():
            print(f"Disconnecting {key}")
            session.disconnect()
        loop.close()
run()
