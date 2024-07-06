import Twitch_Edog0049a as Twitch
from threading import Thread
from Twitch_Edog0049a.ChatInterface.TwitchChatInterface import TCISettings
from typing import Dict, List, Callable
from queue import Queue
from .Builtins.user import User
from ChatSession.Settings import TWITCH_CHAT_PORT, TEST_MODE
from ChatSession.Settings import TWITCH_CHAT_URL, TWITCH_CHAT_CAPABILITIES, TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET
from .utilis import runCallback
from .chatParser import parser
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
        self._chatSettingsLoaded: bool = False
        self._twitchChat = Twitch.Chat(self._loadChatSettings())
        self._error = None
        self._chatUsers: List = []
        self.botInfo = None
        self.streamerInfo = None
        self._parser = parser(self)
    
        ############################# Event Subscriptions #############################
        self._twitchChat.onMessage(self._parser.parse)
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
        #self._user.updateCommands()
        self._user.clearCache()
        self._twitchChat.disconnect()

    def startChatClient(self) -> None:
        if not self._twitchChat.isConnected and self._chatSettingsLoaded:
            self._user.cacheAllComands()
            self._twitchChat.start()                 
            self._twitchChat.connect()
    
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
        self._chatSettingsLoaded = self._hasRequiredChatSettings
        if self._chatSettingsLoaded:
            settings = {
                'channels': [self._user.settings.Streamer],
                'user' : self._user.settings.BotUser,
                'password' : self._user.settings.BotOAuth
            }
        else:
            settings={}
        return TCISettings(**settings)
    
    def _hasRequiredChatSettings(self):
        return self._user.settings.BotOAuth and self._user.settings.BotUser and self._user.settings.Streamer
    
    def _updateChatSettings(self) -> None:
        self._user.loadSettings()
        reconnect = self._twitchChat.isConnected
        if self._twitchChat.isConnected:
            self.disconnect()
        self._twitchChat.updateSettings(self._loadChatSettings())
        if reconnect and self._chatSettingsLoaded:
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
