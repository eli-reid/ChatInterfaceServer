
COMMAND_DB = "Commands_commands"
CHAT_SETTINGS_DB = "Chat_chatsettings"


class SETTINGS_SQL:
    GET = f"SELECT * FROM {CHAT_SETTINGS_DB} WHERE user_id=?"


class COMMANDS_SQL:
    SELLECT_ALL_BY_USER_ID = f"SELECT * FROM {COMMAND_DB} WHERE user_id=?"
    UPDATE = f"UPDATE Commands_commands(command, data, cooldown, \
                roleRequired, usage, enabled, lastUsed) VALUES ('?','?',?,'?','?',?,'?') \
                    WHERE user_id=? AND id=?"
    ADD = "INPUT INTO Commands_commands(command, user_id, data, cooldown, roleRquired, usage, enabled)\
            VALUES ('?', ?, '?', '?', '?','?','?')"
            
