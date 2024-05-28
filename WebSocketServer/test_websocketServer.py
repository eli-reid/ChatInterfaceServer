import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from websockets import ConnectionClosedError
from websockets.server import WebSocketServerProtocol
from src.EventHandler import EventHandler
from .WebsocketServer import WebSockServer

# Helper function to run coroutines in the test
def run_coroutine(coroutine):
    return asyncio.get_event_loop().run_until_complete(coroutine)

@pytest.mark.parametrize("message, path, client_count, expected_send_calls", [
    (b"Hello, World!", "/test", 3, 3),  # TC_ID_01: All clients receive the message
    (b"", "/empty", 2, 2),              # TC_ID_02: Send empty message to all clients
    (b"Data", "/single", 1, 1),         # TC_ID_03: Single client receives a message
])
def test_broadcast(message, path, client_count, expected_send_calls):
    # Arrange
    server = WebSockServer()
    clients = {AsyncMock(spec=WebSocketServerProtocol) for _ in range(client_count)}
    server._clients[path] = clients
    server.send = AsyncMock(return_value=True)

    # Act
    run_coroutine(server.broadcast(message, path))

    # Assert
    assert server.send.call_count == expected_send_calls
    for client in clients:
        server.send.assert_any_call(message, client)

@pytest.mark.parametrize("message, websocket, expected_result", [
    (b"Hello", AsyncMock(spec=WebSocketServerProtocol), True),  # TC_ID_04: Successful send
    (b"Hello", AsyncMock(spec=WebSocketServerProtocol, send=AsyncMock(side_effect=ConnectionClosedError)), False),  # TC_ID_05: Connection closed error
    (b"Hello", AsyncMock(spec=WebSocketServerProtocol, send=AsyncMock(side_effect=Exception("Error"))), False),  # TC_ID_06: General exception
])
def test_send(message, websocket, expected_result):
    # Arrange
    server = WebSockServer()

    # Act
    result = run_coroutine(server.send(message, websocket))

    # Assert
    assert result == expected_result

@pytest.mark.parametrize("path, expected_clients", [
    ("/test", {AsyncMock(spec=WebSocketServerProtocol)}),  # TC_ID_07: Path with one client
    ("/empty", set()),                                    # TC_ID_08: Path with no clients
])
def test_getClients(path, expected_clients):
    # Arrange
    server = WebSockServer()
    server._clients[path] = expected_clients

    # Act
    clients = run_coroutine(server.getClients(path))

    # Assert
    assert clients == expected_clients

@pytest.mark.parametrize("path, clients", [
    ("/test", {AsyncMock(spec=WebSocketServerProtocol)}),  # TC_ID_09: Update non-empty client set
    ("/empty", set()),                                    # TC_ID_10: Update empty client set
])
def test_updateClients(path, clients):
    # Arrange
    server = WebSockServer()

    # Act
    run_coroutine(server.updateClients(path, clients))

    # Assert
    if clients:
        assert server._clients[path] == clients
    else:
        assert path not in server._clients

@pytest.mark.parametrize("path, websocket", [
    ("/test", AsyncMock(spec=WebSocketServerProtocol)),  # TC_ID_11: Add client to path
])
def test_addClient(path, websocket):
    # Arrange
    server = WebSockServer()

    # Act
    run_coroutine(server.addClient(path, websocket))

    # Assert
    assert websocket in server._clients[path]
    
    
class AsyncIterator:
    def __init__(self, seq):
        self.iter = iter(seq)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.iter)
        except StopIteration as e:
            raise StopAsyncIteration from e
        


@pytest.mark.parametrize("websocket, path, message", [
    (AsyncMock(spec=WebSocketServerProtocol, spec_set=AsyncIterator([b"Message"])), "/test", b"Message"),  # TC_ID_12: Handle incoming message
])
def test_messageHandler(websocket, path, message):
    # Arrange
    server = WebSockServer()
    server.addClient = AsyncMock()
    server.event = EventHandler()
    server.event.on = AsyncMock()

    # Act
    run_coroutine(server._messageHandler(websocket, path))

    # Assert
    server.addClient.assert_called_once_with(path, websocket)
    #server.event.on.assert_called_once_with(server, 'message', message)

# Test for server start and message handling
def test_start():
    # Arrange
    server = WebSockServer()
    server._server = AsyncMock()

    # Act
    run_coroutine(server.start())

    # Assert
    server._server.assert_called_once()