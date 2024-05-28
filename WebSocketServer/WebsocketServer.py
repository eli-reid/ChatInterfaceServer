from websockets import ConnectionClosedError, server 
from threading import Thread
from typing import Optional
import websockets
import asyncio
from websockets.server import serve, WebSocketServerProtocol
from collections import defaultdict
from src.EventHandler import EventHandler
import logging
import pickle


class WebSockServer:
    def __init__(self, url: str = 'localhost', port: int=8001) -> None:
        self.event: EventHandler = EventHandler()
        self._clients: dict[str, set] = defaultdict(set)
        self._url: str = url
        self._port: int = port
        self._lock = asyncio.Lock()
    
    async def broadcast(self, message: bytes, path: str)->None:
        print(f"Broadcasting message {message} to {path}")
        clients = await self.getClients(path)
        deadClients = set()
        for websocket in clients:
            if not await self.send(message, websocket):
                deadClients.add(websocket)
        clients.difference_update(deadClients)
        await self.updateClients(path, clients)

    
    async def send(self, message: bytes, websocket)->bool:
        try:
            await websocket.send(message)
            return True
        except ConnectionClosedError as e:
            return False
        except Exception as e:
            logging.error(f"Error: {e}")
        return False

   
    async def getClients(self, path: str)->set:
        async with self._lock:
            if path not in self._clients:
                self._clients[path] = set()
            return self._clients.get(path).copy()
            
    
    async def updateClients(self, path: str, clients: set)->None:
        async with self._lock:
            if clients:
                self._clients[path] = clients
            elif path in self._clients:
                del self._clients[path]
    
    async def addClient(self, path: str, websocket: WebSocketServerProtocol)->None:
        async with self._lock:
            self._clients[path].add(websocket)
            print(f"Adding client {websocket.remote_address} with path {path}")
         
    async def _messageHandler(self, websocket: WebSocketServerProtocol, path: str):
        async for message in websocket:
            await self.addClient(path, websocket)
            data = pickle.loads(message)
            data["websocket"] = websocket
            self.event.emit(self, 'message', data )
            
    async def _server(self):
        self.server = await websockets.serve(self._messageHandler, self._url, self._port)
        if self.server.is_serving:
            print(f"Server started at {self._url}:{self._port}")
        
        #asyncio.create_task(self.checkConnections())
        await self.server.serve_forever()
    
    async def start(self):

        await self._server()
       
    async def stop(self):
        await self._server.close()
        print("Server stopped")
        
    async def checkConnections (self):
        
        print("Checking connections")
        deadClients = set()
        while self.server.is_serving:
            async with self._lock:
                clients = self._clients.copy()
            print("Checking connections...")
            print(clients)
            for connection in clients:
                for websocket in clients[connection]:
                    try:
                        await websocket.ping()
                        print(f"Connection alive: {websocket.remote_address}")
                    except (websockets.exceptions.ConnectionClosedOK,
                            websockets.exceptions.ConnectionClosed, 
                            websockets.exceptions.ConnectionClosedError
                            ) as e:
                        deadClients.add(websocket)
                        print(f"Connection closed: {websocket.remote_address}")
                if deadClients:
                    clients[connection].difference_update(deadClients)
                    await self.updateClients(connection, clients[connection])
            await asyncio.sleep(10)
 
        