
import os

TWITCH_CHAT_URL ="irc.chat.twitch.tv"
TWITCH_CHAT_PORT = 6667
TWITCH_CHAT_CAPABILITIES = ["twitch.tv/tags", "twitch.tv/commands", "twitch.tv/membership"]
TWITCH_CLIENT_ID = os.environ.get("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.environ.get("TWITCH_CLIENT_SECRET")

CHAT_SESSIONS = {}

TEST_MODE = False