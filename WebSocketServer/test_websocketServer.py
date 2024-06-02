import pytest
import asyncio
from websockets import ConnectionClosedError
from websockets.server import WebSocketServerProtocol
from unittest.mock import AsyncMock, MagicMock, patch
from .WebsocketServer import WebSockServer
import random

# Helper function to run async tests
def run_async(func):
    return asyncio.get_event_loop().run_until_complete(func)

# Test for broadcasting messages to multiple clients
@pytest.mark.parametrize("message, path, client_count, expected_send_calls", [
    (b"Hello, World!", "/test", 3, 3),  # TC01: Happy path with 3 clients
    (b"", "/empty", 2, 2),              # TC02: Empty message with 2 clients
    (b"Data", "/none", 0, 0),           # TC03: No clients connected
])
def test_broadcast(message, path, client_count, expected_send_calls):
    # Arrange
    server = WebSockServer()
    clients = {AsyncMock(spec=WebSocketServerProtocol) for _ in range(client_count)}
    server._clients[path] = clients

    # Act
    run_async(server.broadcast(message, path))

    # Assert
    actual_send_calls = sum(1 for client in clients if client.send.call_count == 1)
    assert actual_send_calls == expected_send_calls, "All clients should receive the message exactly once."

# Test for handling client disconnections during message sending
@pytest.mark.parametrize("message, path, client_count, disconnect_count, expected_remaining_clients", [
    (b"Update", "/test", 5, 2, 3),  # TC04: 2 out of 5 clients disconnect
    (b"Update", "/test", 3, 3, 0),  # TC05: All clients disconnect
])
def test_handle_disconnections(message, path, client_count, disconnect_count, expected_remaining_clients):
    # Arrange
    server = WebSockServer()
    clients = {AsyncMock(spec=WebSocketServerProtocol) for _ in range(client_count)}
    disconnect_clients = set(list(clients)[:disconnect_count])
    for client in disconnect_clients:
        client.send.side_effect = ConnectionClosedError
    server._clients[path] = clients

    # Act
    run_async(server.broadcast(message, path))

    # Assert
    assert len(server._clients[path]) == expected_remaining_clients, "Only connected clients should remain."

# Test for adding a new client
@pytest.mark.parametrize("path, initial_count, add_count", [
    ("/test", 0, 1),  # TC06: Add first client
    ("/test", 1, 1),  # TC07: Add another client
])
def test_add_client(path, initial_count, add_count):
    # Arrange
    server = WebSockServer()
    server._clients[path] = {AsyncMock(spec=WebSocketServerProtocol) for _ in range(initial_count)}
    new_clients = [AsyncMock(spec=WebSocketServerProtocol) for _ in range(add_count)]

    # Act
    for client in new_clients:
        run_async(server.addClient(client, path))

    # Assert
    assert len(server._clients[path]) == initial_count + add_count, "All new clients should be added."

# Test for server start and stop
def test_server_start_stop():
    # Arrange
    server = WebSockServer(port=8111)
    server.server = AsyncMock()

    # Act
    run_async(server.start())
    run_async(server.stop())

    # Assert
    server.server.close.assert_called_once(), "Server should be closed properly."
    assert server.server.is_serving == False, "Server should not be serving after stop."
