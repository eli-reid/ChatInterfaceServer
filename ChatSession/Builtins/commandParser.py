from datetime import datetime
from .dataObjects import commandObj
from typing import Dict
class CommandParser:
    def parseNewCommand(self, commandData: list, user_id) -> commandObj: 
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
        roleDict: dict = {
            "+b": "broadcaster",
            "+m": "moderator",
            "+e": "editor",
            "+s": "subscriber",
            "+a": "any"
       }
        
        usageDict: dict ={
            "SC": "stream chat",
            "SW": "stream whisper",
            "SB": "stream both"
        } 
        
        command = commandData.pop(0)
        for key, value in roleDict.items():
            if key in commandData:
                roleRequired = value
                commandData.remove(key)
                break
            
        for key, value in usageDict.items():    
            if key in commandData:
                usage = value
                commandData.remove(key)
                break
            
        cooldownIndex: int = commandData.index("+cd") + 1 if "+cd" in commandData else -1
        
        if "+cd" in commandData:
            if  0 < cooldownIndex < len(commandData) and commandData[cooldownIndex].isdigit():
                cooldown = commandData.pop(cooldownIndex)
            commandData.pop(commandData.index("+cd"))
        else:
            cooldown = 5
              
        return commandObj(id=-1,
                          data=" ".join(commandData), 
                          roleRequired="any" if roleRequired is None else roleRequired,
                          usage="stream chat" if usage is None else usage,
                          cooldown=cooldown,
                          enabled=True,
                          lastUsed=datetime.now(),
                          user_id=user_id,
                          command=command
                          )
        
    
    def parseCommand(self,tci, message , commandData) -> str:
        
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
            "$targetid": message,
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
        