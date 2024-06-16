import asyncio
import contextlib
from typing import Awaitable, Optional
import websockets
import logging
from websockets.client import WebSocketClientProtocol
from EventHandler_Edog0049a import EventHandler
from enum import Enum
class WebsocketClient:
    TIMERDEFAULT =.1
    class EVENTENUM():
        CONNECTED: str =  "Connected"
        DISCONNECTED: str = "Disconnected"
        RECONNECTED: str  = "Reconnected"
        RECONNECTING: str  = "Reconnecting"
        MESSAGE: str  = "Message"
        MESSAGEFAI: str = "MessageFailed"

    def __init__(self, url: str, consumer: Awaitable, producer: Awaitable, autoReconnect:bool=True, maxRetries:Optional[int]=-1) -> None:
        
        self.events: EventHandler = EventHandler()
        self._connection: WebSocketClientProtocol = None
        self._consumer: Awaitable = consumer   
        self._producer: Awaitable = producer
        self._url:str = url
        self._autoReconnect: bool = autoReconnect
        self._reconnectTimer: float = self.TIMERDEFAULT
        self._reconnecting: bool = False
        self._retries: int = maxRetries
        self._messageFailed: bool = False
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

    async def disconnect(self):
        self._autoReconnect = False
        with contextlib.suppress(AttributeError):
            await self._connection.close()
        
    def connect(self):
        task = self.loop.create_task(self._connect(), name="WebsocketClient")
    
    async def aConnect(self):
        await self._connect()
   
    async def _connect(self):
        try:
            async with websockets.connect(self._url) as self._connection:
                self._reconnectTimer = self.TIMERDEFAULT
                self._reconnect = self._autoReconnect
                self.events.emit(self,self.EVENTENUM.CONNECTED,"connected")
                self._reconnecting = False
                await asyncio.gather(
                    self._consumerHandler(),
                    self._producerHandler()
                    )
                await asyncio.Future()
        except (
                websockets.exceptions.ConnectionClosed,
                websockets.exceptions.ConnectionClosedError,
                websockets.exceptions.ConnectionClosedOK
                ) as reason:
            self.events.emit(self,self.EVENTENUM.DISCONNECTED, reason)
            print(f"REASON: {reason}")
        
        finally:
            if self._autoReconnect and not self._reconnecting:
                await self.reconnect()

    async def reconnect(self) -> bool:
        triesLeft = self._retries
        self._reconnecting = True
        while self._autoReconnect and triesLeft!=0:
            print(f"RECONNECTING{triesLeft}")
            try: 
                self.events.emit(self,self.EVENTENUM.RECONNECTING)
                await asyncio.sleep(self._reconnectTimer)
                self._reconnectTimer = self._reconnectTimer * 2
                await self._connect()
                return True
            except Exception as e:
                if triesLeft > 0:
                    triesLeft -= 1
                else:
                    self.events.emit(self, str(self.EVENTENUM.DISCONNECTED), e)
                    self.stopReconnect()
        return False        
            
    def stopReconnect(self): 
        self._autoReconnect = False
    
    def autoReconnect(self):
        self._autoReconnect = True

    async def _consumerHandler(self):
        async for message in self._connection:
            self.events.emit(self, str(self.EVENTENUM.MESSAGE), message)
            await self._consumer(message)
            await asyncio.sleep(0)
                
    async def _producerHandler(self):
        while self._connection.open:
            message = await self._producer()
            if message is not None:
                try:
                    await self._connection.send(message)
                except websockets.ConnectionClosed:
                    if await self.reconnect():
                        while not self._connection.open: 
                            await asyncio.sleep(0)
                        await self._connection.send(message)
                    else:
                        self.events.emit(self, self.EVENTENUM.MESSAGEFAIL, message)
            await asyncio.sleep(0)

   
   
