import Twitch_Edog0049a as Twitch
from ChatSession.Builtins import *
from abc import ABCMeta

class parser:
    def __init__(self, chatSession) -> None:
        self._chatSession = chatSession
        self._user = self._chatSession._user

    def parse(self, sender,  message: Twitch.MessageType) -> None:
        if message.text is not None and message.text.startswith("!"):
            commandText = message.text.split(" ")[0]
            cmd = globals().get(commandText[1:])    
            if isinstance(cmd, ABCMeta) and issubclass(cmd, commandBase) and commandText != "commandBase":
                try:
                    cmd(self._chatSession._twitchChat, message, self._user) 
                except Exception as e:
                    print(f"Error: {e.args}")#change to log
                    
        elif message.text is not None:
            command(self._chatSession._twitchChat, message, self._user).run(message.text.split(" ")[0])
                