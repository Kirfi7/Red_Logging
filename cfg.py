import vk_api
import sqlite3

from vk_api.bot_longpoll import VkBotLongPoll

TOKEN = "vk1.a.y7jZVoqd0_HqNWZTEzS6hLwEp9Rb9Yu5I7DPc7hWXk5UB5qP7d9bpIFZVBJL6iaAcsvS5xKAN5CnQYSNXX89TBXCuK7cS1NOfnMePmQ6-d5dmtDz_rGRq4K4DtrImAUvSqdoopX_7Hs4Rq2fZx1-PR1GMN_hwos5VgKUgVcPeoU1x_0dtsj65oBp9U_NuYAnbogGdMdUS-Fy-Tzr0p4OCg"
# group token

DEV = ["534422651", "468509613"]
#         Миша          Кирилл

STAFF = ["327113505", "16715256", "137480835"]
#           Влад         Гей         Серый

CONST = 2

COMMANDS = {
    "mute": {"lvl": 1, "parameters": 4},
    "unmute": {"lvl": 1, "parameters": 3},
    "jail": {"lvl": 1, "parameters": 4},
    "unjail": {"lvl": 1, "parameters": 3},
    "warn": {"lvl": 2, "parameters": 3},
    "unwarn": {"lvl": 2, "parameters": 3},
    "ban": {"lvl": 3, "parameters": 4},
    "unban": {"lvl": 3, "parameters": 3},
    "permban": {"lvl": 4, "parameters": 3},
    "ungwarn": {"lvl": 3, "parameters": 4}
}

# db = sqlite3.connect('admins.db')
# c = db.cursor()
# c.execute(f"CREATE TABLE admins (nick TEXT, lvl INTEGER, vk_id INTEGER)")
# db.commit()
# db.close()
#
# db = sqlite3.connect('forms.db')
# c = db.cursor()
# c.execute(f"CREATE TABLE forms (form TEXT, lvl INTEGER, date INTEGER, vk_id INTEGER)")
# db.commit()
# db.close()

vk_session = vk_api.VkApi(token=TOKEN)


def chat_sender(for_chat_id, message_text):
    vk_session.method("messages.send", {
        "chat_id": for_chat_id,
        "message": message_text,
        "random_id": 0
    })
