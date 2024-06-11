
class quoteObj:
    def __init__(self, id, created, quote:str) -> None:
        self.id = id
        self.quote = quote
        self.created = created

class commandObj:
    def __init__(self, data:str=None, roleRequired:str=None, usage:str=None, cooldown:int=None, enabled:bool=None, lastUsed=None, user=None, command=None) -> None:
        self.command = command
        self.data = data
        self.roleRequired = roleRequired
        self.usage = usage
        self.cooldown = cooldown
        self.enabled = enabled
        self.lastUsed = lastUsed
        self.user = user
    
class streamTimerObj:
    def __init__(self, time, displayMsg, endMsg, token) -> None:
        self.time = time
        self.displayMsg = displayMsg
        self.endMsg = endMsg
        self.token = token
  
