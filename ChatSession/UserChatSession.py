import abc
import asyncio
import Twitch_Edog0049a as Twitch
from Twitch_Edog0049a.ChatInterface.TwitchChatInterface import TCISettings
from typing import Dict, List, Callable
from queue import Queue
from .Builtins.commandBase import commandBase
from .Builtins.quote import quote
from .Builtins.dataObjects import commandObj, quoteObj
from .Builtins.command import command
from .Builtins.timer import timer
from .Database.DatabaseInterface import DatabaseInterface
from .Builtins.user import User
from ChatSession.Settings import TWITCH_CHAT_PORT, TEST_MODE
from ChatSession.Settings import TWITCH_CHAT_URL, TWITCH_CHAT_CAPABILITIES, TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET
from .utilis import runCallback
    
#TODO: 
# 1. Add a way to get the chat users from the chat
# 2. store the chat users in the database
# 3. Add a way to get the chat users from the database  
    
class UserChatSession:
    def __init__(self, user: User) -> None:
        self.scopes: List = [
            Twitch.Scope.Channel.Read.Subscriptions,
            Twitch.Scope.Channel.Edit.Commercial,
            Twitch.Scope.Channel.Manage.Moderators,
            Twitch.Scope.Channel.Manage.Broadcast,
            Twitch.Scope.Channel.Manage.Vips,
            Twitch.Scope.Channel.Manage.Raids,
            Twitch.Scope.Bits.Read,
            Twitch.Scope.Moderation.Read,
            Twitch.Scope.Moderator.Read.Chatters,
            Twitch.Scope.Moderator.Read.Followers,
            Twitch.Scope.Moderator.Manage.Announcements,
            Twitch.Scope.Moderator.Manage.Banned_users,
            Twitch.Scope.Moderator.Manage.Chat_messages,
            Twitch.Scope.Moderator.Manage.Shoutouts,
            Twitch.Scope.Moderator.Manage.Chat_settings,
            Twitch.Scope.User.Manage.Chat_color,
            Twitch.Scope.User.Manage.Whispers,        
        ]
    
        self.API: Twitch.Api = None
        self._user = user 
        self._messageQ: Queue = Queue(50)
        self._twitchChatSettingsLoaded: bool = False
        self._twitchChat = Twitch.Chat(self._loadChatSettings())
        self._error = None
        self._chatUsers: List = []
        self.botInfo = None
        self.streamerInfo = None
    
        ############################# Event Subscriptions #############################
        self._twitchChat.onMessage(self._parser)
        self._twitchChat.onReceived(self._onRecieved)
        self._twitchChat.onLoginError(self._onLoginError)
        self._twitchChat.onConnected(self._onConnected)
        self._twitchChat.onDisconnected(self._onDisconnected)
       
        ############################# Event Callbacks #############################
        self.onMessage: Callable = lambda sender, message: None
        self.onLoginFail: Callable = lambda sender, message: None
        self.onError: Callable = lambda sender, message: None
        self.onConnected: Callable = lambda sender, message: None
        self.onDisconnected: Callable = lambda sender, message: None
       
    def disconnect(self) -> None:
        self._user.updateCommands()
        self._user.clearCache()
        self._twitchChat.disconnect()

    def startChatClient(self) -> None:
        if not self._twitchChat.isConnected and self._twitchChatSettingsLoaded:
            self._user.cacheAllComands()
            self._twitchChat.start()     
            self._twitchChat.connect()
            
    def _parser(self, sender,  message: Twitch.MessageType) -> None:
        if message.text is not None and message.text.startswith("!"):
            commandText = message.text.split(" ")[0]
            cmd = globals().get(commandText[1:])    
            if isinstance(cmd, abc.ABCMeta) and issubclass(cmd, commandBase) and commandText != "commandBase":
                try:
                    cmd(self._twitchChat, message, self._user)
                except Exception as e:
                    print(f"Error: {e.args}")#change to log
                    
        elif message.text is not None:
            command(self._twitchChat, message, self._user).run(message.text.split(" ")[0])     
    
    @property
    def status(self) -> Dict:
        return {
            "connected": self._twitchChat.isConnected,
            "error": self.error,
            "bot": self._user.settings.BotUser,
            "streamer": self._user.settings.Streamer,
        }
    
    @property
    def isConnected(self) -> bool:
        return self._twitchChat.isConnected
    
    @property
    def error(self) -> str:
        err = self._error
        self._error = None
        return err
    
    @error.setter
    def error(self, value: str) -> None:
        self._error = value
        if value is not None:
            self._runCallback(self.onError, self, value)
            
    def _loadChatSettings(self) -> TCISettings:
        if self._user.settings.BotOAuth and self._user.settings.BotUser and self._user.settings.Streamer:
            self._twitchChatSettingsLoaded = True
            return TCISettings(server=TWITCH_CHAT_URL, 
                                port=TWITCH_CHAT_PORT, 
                                caprequest=TWITCH_CHAT_CAPABILITIES, 
                                user=self._user.settings.BotUser, 
                                password=self._user.settings.BotOAuth, 
                                channels=[self._user.settings.Streamer,],
                                SSL=False
                            )
        else:
            self._twitchChatSettingsLoaded = False
            return TCISettings()
    
    def _updateChatSettings(self) -> None:
        self._user.loadSettings()
        reconnect = self.isConnected
        if self.isConnected:
            self.disconnect()
            self._twitchChat.updateSettings(self._loadChatSettings())
            if reconnect and self._twitchChatSettingsLoaded:
                self.startChatClient()

    ############################# Event Handlers #############################
    def _onLoginError(self, sender, message) -> None:
        self.error = message
        runCallback(self.onLoginFail, sender, message)
        self.disconnect()

    def _onRecieved(self, sender, message: Twitch.MessageType) -> None:
        runCallback(self.onMessage, sender, message)

    def _onConnected(self, sender, message) -> None:
        runCallback(self.onConnected, sender, message)

    def _onDisconnected(self, sender, message) -> None:
        runCallback(self.onDisconnected, sender, message)
