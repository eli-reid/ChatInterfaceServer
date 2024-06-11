import websockets
import asyncio
from websockets.server import serve, WebSocketServerProtocol
from websockets.exceptions import ConnectionClosed, ConnectionClosedError, ConnectionClosedOK
from collections import defaultdict
from src.EventHandler import EventHandler


class WebSockServer:
    def __init__(self, url: str = 'localhost', port: int=8001) -> None:
        self.event = EventHandler()
        self._clients = defaultdict(set)
        self._url = url
        self._port = port
        self._lock = asyncio.Lock()
        
    async def broadcast(self, message: bytes, path: str)->None:
        clients = await self.getClientsCopy(path)
        deadClients = await self.sendToClients(message, clients)
        await self.updateClients(path, clients.difference(deadClients))
    
    async def sendToClients(self, message: bytes, clients: set) -> set:
        deadClients = set()
        for clientSocket in clients:
            if not await self.send(message, clientSocket):
                deadClients.add(clientSocket)
        return deadClients
    
    async def send(self, message: bytes, clientSocket: WebSocketServerProtocol)->bool:
        try:
            await clientSocket.send(message)
            return True
        except (ConnectionClosedError, ConnectionClosed, ConnectionClosedOK):
            return False

    async def getClientsCopy(self, path: str)->set:
        async with self._lock:
            return self._clients.setdefault(path, set()).copy()
            
    async def updateClients(self, path: str, clients: set)->None:
        async with self._lock:
            if clients:
                self._clients[path] = clients
            else:
                self._clients.pop(path, None)
    
    async def addClient(self, clientSocket: WebSocketServerProtocol, path: str)->None:
        async with self._lock:
            self._clients[path].add(clientSocket)

    async def _messageHandler(self, clientSocket: WebSocketServerProtocol, path: str) -> None:
        await self.addClient(clientSocket, path)
        print(f"Client connected to {path}")
        try:
            async for message in clientSocket:
                self.event.emit(self, 'message', (path,message))
        except (ConnectionClosedError, ConnectionClosed, ConnectionClosedOK):
            async with self._lock:
                self._clients[path].remove(clientSocket)
            
    async def start(self):
        self.server = await websockets.serve(self._messageHandler, self._url, self._port)
        if self.server.is_serving:
            print(f"Server started at {self._url}:{self._port}")
        await self.server.serve_forever()
    
    async def stop(self):
        await self.server.close()
        print("Server stopped")        