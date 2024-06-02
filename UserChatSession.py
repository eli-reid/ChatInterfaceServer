import abc
import asyncio
import Twitch
from threading import Thread
from Twitch.ChatInterface.TwitchChatInterface import TCISettings
from typing import Dict, List, Callable, Coroutine
from queue import Queue
from Builtins.commandBase import commandBase 
from Builtins.command import command
from Settings import TWITCH_CHAT_PORT, TEST_MODE
from Settings import TWITCH_CHAT_URL, TWITCH_CHAT_CAPABILITIES, TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET
from DatabaseInterface import DatabaseInterface
    
#TODO: 
# 1. Add a way to get the chat users from the chat
# 2. store the chat users in the database
# 3. Add a way to get the chat users from the database  
class User:
    def __init__(self, id, name, key) -> None:
        self.id = id
        self.name = name
        self.key = key
        self.commands = None
        
class UserSettings:
    def __init__(self) -> None:
        self.BotUser = None
        self.BotOAuth = None
        self.Streamer = None
        self.StreamerOAuth = None

    
class UserChatSession:

    def __init__(self, user) -> None:
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
        self.botInfo = None
        self.streamerInfo = None
        self._user = user 
        self._messageQ: Queue = Queue(50)
        self._twitchChat: Twitch.Chat = Twitch.Chat()
        self._error = None
        self.settings = UserSettings()
        self._chatUsers: List = []
        self.loadTwitchChatSettings()

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
       

    @property
    def status(self) -> Dict:
        return {
            "connected": self._twitchChat.isConnected,
            "error": self.error,
            "bot": self.settings.BotUser,
            "streamer": self.settings.Streamer,
        }
    
    @property
    def isConnected(self) -> bool:
        return self._twitchChat.isConnected
    
    @property
    def _getStreamerOAuthToken(self) -> Twitch.Credentials:
        if self.settings.BotOAuth is not None:
            return self.settings.BotOAuth.replace("oauth:","")
        return None
    
    @property
    def error(self) -> str:
        return self._error
    
    @error.setter
    def error(self, value: str) -> None:
        self._error = value
        if value is not None:
            self._runCallback(self.onError, self, value)

    
    def disconnect(self) -> None:
        self._twitchChat.run = False
        self._twitchChat.disconnect()


    def loadTwitchChatSettings(self) -> None:
        dbConnector = DatabaseInterface("D:\\FoxZBot2\\Fox_Z_Bot\\db.sqlite3")
        data = dbConnector.fetch(f"SELECT * FROM Chat_chatsettings WHERE User_id={self._user.id}").fetchone()
        dbConnector.close()
        self.settings.BotOAuth = data[1]
        self.settings.BotUser = data[2]
        self.settings.Streamer = data[3]
        self.settings.StreamerOAuth = data[4]
 
        if self.settings.BotOAuth and self.settings.BotUser and self.settings.Streamer:
            reconnect = self.isConnected
        
            if self.isConnected:
                self.disconnect()

            chatSettings = TCISettings(server=TWITCH_CHAT_URL, 
                                            port=TWITCH_CHAT_PORT, 
                                            caprequest=TWITCH_CHAT_CAPABILITIES, 
                                            user=self.settings.BotUser, 
                                            password=self.settings.BotOAuth, 
                                            channels=[self.settings.Streamer,],
                                            SSL=False)
            self._twitchChat.updateSettings(chatSettings)
            if reconnect:
                self.startChatClient()
        

    def startChatClient(self) -> None:
        if not self._twitchChat.isConnected:
            self.error = None
            self._twitchChat.run = True
            sendMsgThread = Thread(target=self._twitchChat.sendMsgFunction)
            recieveMsgThread = Thread(target=self._twitchChat.receiveMsgFunction)
            sendMsgThread.start()
            recieveMsgThread.start()            
            self.error = None
            self._twitchChat.connect()

   
    def _parser(self, sender,  message: Twitch.MessageType) -> None:
        if message.text is not None: 
            commandText = message.text.split(" ")[0]
            cmd = globals().get(commandText[1:])    
            if isinstance(cmd, abc.ABCMeta) and issubclass(cmd, commandBase) and commandText != "commandBase":
                try:
                    cmd(self._twitchChat, message, self._user)
                except Exception as e:
                    print(f"Error: {e.args}")#change to log
            elif message.text is not None:
                command(self._twitchChat, message, self._user).run(message.text.split(" ")[0])


    def addChatUser(self, message: Twitch.MessageType) -> None:
        msgUserInfo: dict = {}
        msgparts = message.raw.split(";")
        for part in msgparts:
            key, value = part.split("=")
            msgUserInfo[key] = value
        chatUser = self._user.chatusers.get_or_create(username=message.username, room=message.channel)[0]
        chatUser.userId = msgUserInfo["user-id"]
        chatUser.isMod = msgUserInfo["mod"]
        chatUser.isBroadcaster = msgUserInfo["user-id"] == msgUserInfo["room-id"]
        chatUser.isSub = msgUserInfo["subscriber"]
        chatUser.isEditor = msgUserInfo["turbo"]
        chatUser.save()


    
    ############################# Helper Functions #############################
    def _runAsyncFunction(self, func: Coroutine ,*args, **kwargs) -> any:
        try:
            loop = asyncio.new_event_loop()
            return loop.run_until_complete(func(*args, **kwargs))
        except Exception as e:
            print(f"_runAsyncFunction Error: {e.args}")
            return None
        
    def _runCallback(self, func: Callable, *args, **kwargs) -> None:
        if asyncio.iscoroutinefunction(func):
            self._runAsyncFunction(func, *args, **kwargs)
        else:
            func(*args, **kwargs)

    ############################# Event Handlers #############################
    def _onLoginError(self, sender, message) -> None:
        self.error = message
        self._runCallback(self.onLoginFail, sender, message)
        self.disconnect()

    def _onRecieved(self, sender, message: Twitch.MessageType) -> None:
        self._runCallback(self.onMessage, sender, message)

    def _onConnected(self, sender, message) -> None:
        self._runCallback(self.onConnected, sender, message)

    def _onDisconnected(self, sender, message) -> None:
        self._runCallback(self.onDisconnected, sender, message)
    

