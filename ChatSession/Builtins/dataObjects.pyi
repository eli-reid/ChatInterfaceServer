from _typeshed import Incomplete
from typing import TypeVar

class quoteObj:
    id: Incomplete
    quote: Incomplete
    created: Incomplete
    def __init__(self, id, created, quote: str) -> None: ...
L = TypeVar('L')

class commandObj:
    id: Incomplete
    command: Incomplete
    data: Incomplete
    roleRequired: Incomplete
    usage: Incomplete
    cooldown: Incomplete
    enabled: Incomplete
    lastUsed: Incomplete
    user_id: Incomplete
    def __init__(self, id: int, data: str, roleRequired: str, usage: str, cooldown: int, enabled: bool, lastUsed: L, user_id: int, command: str) -> None: ...

class streamTimerObj:
    time: Incomplete
    displayMsg: Incomplete
    endMsg: Incomplete
    token: Incomplete
    def __init__(self, time: str, displayMsg: str, endMsg: str, token: str) -> None: ...

class UserSettings:
    BotUser: Incomplete
    BotOAuth: Incomplete
    Streamer: Incomplete
    StreamerOAuth: Incomplete
    def __init__(self, botUser: Incomplete | None = None, botOAuth: Incomplete | None = None, streamer: Incomplete | None = None, streamOAuth: Incomplete | None = None) -> None: ...
