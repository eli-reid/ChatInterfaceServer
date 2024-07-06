from ChatSession.Settings import CHAT_SESSIONS
from WebSocketServer.WebsocketServer import WebSockServer as WS
from MessageParser import MessageParser
import asyncio

async def run():
    try:
        server = WS(port=8011)
        server.event.on('message', MessageParser)
        await server.start()
    except KeyboardInterrupt as e:
        for key, session in CHAT_SESSIONS.items():
            print(f"Disconnecting {key}")
            session.disconnect()
        await server.stop()

asyncio.run(run())
