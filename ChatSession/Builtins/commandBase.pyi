import abc
from Twitch_Edog0049a import ChatInterface as TCI
from Twitch_Edog0049a.ChatInterface.MessageHandler import Message as Message
from _typeshed import Incomplete
from abc import ABC, abstractmethod

class commandBase(ABC, metaclass=abc.ABCMeta):
    message: Incomplete
    tci: Incomplete
    data: Incomplete
    def __init__(self, tci: TCI, message: Message, cmd: str, roleRequire: Incomplete | None = None, cooldown: int = 30, *args, **kwargs) -> None: ...
    @property
    def roleRequired(self): ...
    @abstractmethod
    def add(self): ...
    @abstractmethod
    def remove(self): ...
    @abstractmethod
    def print(self): ...
