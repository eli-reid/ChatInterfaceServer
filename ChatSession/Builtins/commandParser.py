from datetime import datetime
from .dataObjects import commandObj
class CommandParser:
    def parseNewCommand(self, commandData: list, user_id) -> commandObj:  # type: ignore
        """
        cooldown
            +cd - cooldown followed by int
        rolerequired
            +rb - broadcaster
            +rm - mod
            +rs - subscriber
            +ra - any
        usage
            +uc - chatroom only 
            +uw - wisper only
            +ua - any
        """
        role: dict = {
            "+b": "broadcaster",
            "+m": "moderator",
            "+e": "editor",
            "+s": "subscriber",
            "+a": "any"
       }
        
        usage: dict ={
            "SC": "stream Chat",
            "SW": "stream whisper",
            "SB": "stream both"
        } 
       
        cmd = commandObj()
        cmd.command = commandData.pop(0)
        for key, value in role.items():
            if key in commandData:
                cmd.roleRequired = value
                commandData.remove(key)
                break
        for key, value in usage.items():    
            if key in commandData:
                cmd.usage = value
                commandData.remove(key)
                break
        cooldownIndex = commandData.index("+cd") + 1 if "+cd" in commandData else -1
        if "+cd" in commandData:
            if  0 < cooldownIndex < len(commandData) and commandData[cooldownIndex].isdigit():
                cmd.cooldown = commandData.pop(cooldownIndex)
            commandData.pop(commandData.index("+cd"))
        else:
            cmd.cooldown = 5
              
        cmd.data = " ".join(commandData)
        cmd.roleRequired = "any" if cmd.roleRequired is None else cmd.roleRequired
        cmd.usage = "stream Chat" if cmd.usage is None else cmd.usage
        cmd.enabled = True
        cmd.user = user_id
        cmd.lastUsed = datetime.now()
        return cmd
    
    def parseCommand(self,tci, message, commandData) -> str:
        
        """
        
        Parse List
        $userid - Username in lower case
        $username - display Username as normal
        $targetid - targets username in lower case
        $targetname - target username displayed as is
        $randuserid - gets random user from chat
        $botname - displays bot's name
        $arg1-$arg9 - gets position of whats after command
        $math[] - !math [1+7*6]
        $followage - gets months followed streamer 'https://api.twitch.tv/helix/users/follows?to_id=23161357' this gets follwers of a person 
        TODO:
        target
        """      
        parseItems: dict = {
            "$userid": message.username.lower(),
            "$username": message.username,
            "$botname": tci.globalUserState.display_name,
            #"$targetid": self.data[0],
        }
        #parse arguments for message text add to parseItems
        for index, val in enumerate(message.text.split(" ")):
            if index > 9:
                break
            parseItems[f"$arg{index}"] = val

        #parse arguments for command data
        for key, value in parseItems.items():
            commandData = commandData.replace(key, value)

        # handle math function in command data
        if "$math" in commandData:
            commandData = commandData.replace("[[","[")
            commandData = commandData.replace("]]","]")
            mathString = commandData[commandData.index("["):commandData.index("]")+1]
            commandData = commandData.replace("$math","") 
            commandData = commandData.replace(mathString, str(self._parseMath(mathString))) 
        return commandData


    def parseMath(self, mathString: str) -> str:
        try:
            return 1
        finally:
            return 0  
        