import sqlite3
import datetime


def get_nick(user_id):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    nick_name = cursor.execute(f"SELECT nick_name FROM main WHERE vk_id = '{user_id}'").fetchone()[0]
    database.commit()
    database.close()
    return nick_name


def online(user_id):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    status = cursor.execute(f"SELECT online FROM main WHERE vk_id = '{user_id}'").fetchone()[0]
    database.commit()
    database.close()
    return int(status)


def add_online(user_id):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    cursor.execute(f"UPDATE main SET online = '{1}' WHERE vk_id = '{user_id}'")

    time = int(str(datetime.datetime.now().timestamp()).split('.')[0])

    cursor.execute(f"UPDATE main SET time = '{time}' WHERE vk_id = '{user_id}'")
    database.commit()
    database.close()


def del_online(user_id):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    cursor.execute(f"UPDATE main SET online = '{0}' WHERE vk_id = '{user_id}'")
    time = int(cursor.execute(f"SELECT time FROM main WHERE vk_id = '{user_id}'").fetchone()[0])

    uix_now = int(str(datetime.datetime.now().timestamp()).split('.')[0])
    new_time = 0

    cursor.execute(f"UPDATE main SET time = '{new_time}' WHERE vk_id = '{user_id}'")
    database.commit()
    database.close()
    return (uix_now - time) // 60


def clear_online():
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    cursor.execute(f"UPDATE main SET online = '{0}'")
    database.commit()
    database.close()


def change_online(user_id):
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    is_online = int(cursor.execute(f"SELECT online FROM main WHERE vk_id = '{user_id}'").fetchone()[0])

    new_online = 0 if is_online == 1 else 1
    time = 0 if online == 0 else int(str(datetime.datetime.now().timestamp()).split('.')[0])

    cursor.execute(f"UPDATE main SET online = '{new_online}' WHERE vk_id = '{user_id}'")
    cursor.execute(f"UPDATE main SET time = '{time}' WHERE vk_id = '{user_id}'")
    database.commit()
    database.close()

    return new_online


def get_online():
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    online_list = cursor.execute(f"SELECT vk_id, nick_name, time FROM main WHERE online = '{1}'").fetchall()

    uix_now = int(str(datetime.datetime.now().timestamp()).split('.')[0])
    message = "📶 Список администрации онлайн:\n"
    k = 0
    for admin in online_list:
        k += 1
        message += f"— [id{admin[0]}|{admin[1]}] | Минут в сети: {(uix_now - int(admin[2])) // 60}\n"

    message += f"\n🔟 Всего администраторов: {k}"
    return message, k


def get_to(message):
    if "reply_message" in message:
        return str(message['reply_message']['from_id'])

    elif not(message['fwd_messages'] is None):
        return str(message['fwd_messages'][0]['from_id'])

    else:
        return "0"
