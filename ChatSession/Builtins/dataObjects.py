from datetime import datetime
from typing import TypeVar

__all__ = ['commandObj', 'quoteObj', 'streamTimerObj', 'UserSettings']

class quoteObj:
    def __init__(self, id, created, quote:str) -> None:
        self.id = id
        self.quote = quote
        self.created = created
        
L = TypeVar('L')

class commandObj:
    def __init__(self, id: int, data: str, roleRequired: str, usage: str, cooldown: int, enabled: bool, lastUsed: L, user_id: int, command: str ) -> None:
        self.id = id
        self.command = command 
        self.data = data 
        self.roleRequired = roleRequired
        self.usage = usage
        self.cooldown = cooldown
        self.enabled = enabled
        self.lastUsed = lastUsed if lastUsed else datetime.now() 
        self.user_id = user_id
    
class streamTimerObj:
    def __init__(self, time: str, displayMsg: str, endMsg: str, token: str) -> None:
        self.time = time
        self.displayMsg = displayMsg
        self.endMsg = endMsg
        self.token = token
  
class UserSettings:
    def __init__(self,botUser=None, botOAuth=None, streamer=None, streamOAuth=None) -> None:
        self.BotUser = botUser
        self.BotOAuth = botOAuth
        self.Streamer = streamer
        self.StreamerOAuth = streamOAuth