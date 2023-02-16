import time
import vk_api
import sqlite3
import json

from cfg import TOKEN, DEV, STAFF, CONST
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

vk_session = vk_api.VkApi(token=TOKEN)
lp = VkBotLongPoll(vk_session, 218860473)
vk = vk_session.get_api()


def sender(for_chat_id, message_text):
    vk_session.method("messages.send", {
        "chat_id": for_chat_id,
        "message": message_text,
        "random_id": 0,
    })

    # last_message = vk_session.method("messages.getHistory", {
    #     "chat_id": for_chat_id,
    #     "count": 1
    # })["items"][0]
    # message_id = last_message["id"]
    # edited_message = last_message["text"].replace("@red.bottle", "")
    # vk_session.method("messages.edit", {
    #     "chat_id": for_chat_id,
    #     "message_id": message_id,
    #     "message": edited_message,
    #     "dont_parse_links": 1
    # })


while True:
    try:
        for event in lp.listen():
            if event.type == VkBotEventType.MESSAGE_EVENT:

                admin_id = event.obj["user_id"]

                if "reconnect" in event.object.payload.get('type'):
                    sender(2, f"[id{admin_id}|Админ] перезаходит на сервер (тестовое сообщение)")

                elif "disconnect" in event.object.payload.get('type'):
                    sender(2, f"[id{admin_id}|Админ] вышел с сервера (тестовое сообщение)")

                elif "connect" in event.object.payload.get('type'):
                    sender(2, f"[id{admin_id}|Админ] зашел на сервер (тестовое сообщение)")

            if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.chat_id == CONST:

                text = event.object.message['text']
                user_id = event.object.message['from_id']

                if str(user_id) in DEV and text == "add_buttons":
                    keyboard = VkKeyboard(inline=False, one_time=False)
                    keyboard.add_callback_button(
                        label="Зашёл",
                        color=VkKeyboardColor.POSITIVE,
                        payload={"type": f"connect"}
                    )
                    keyboard.add_callback_button(
                        label="Перезахожу",
                        color=VkKeyboardColor.PRIMARY,
                        payload={"type": f"reconnect"},
                    )
                    keyboard.add_callback_button(
                        label="Вышел",
                        color=VkKeyboardColor.NEGATIVE,
                        payload={"type": f"disconnect"}
                    )

                    vk_session.method("messages.send", {
                        "chat_id": CONST,
                        "message": "Секунду...",
                        "keyboard": keyboard.get_empty_keyboard(),
                        "random_id": 0
                    })
                    vk_session.method("messages.send", {
                        "chat_id": chat_id,
                        "message": "Успешно!",
                        "keyboard": keyboard.get_keyboard(),
                        "random_id": 0
                    })

    except Exception as error:
        print(error)
