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
        "disable_mentions": 1,
        "dont_parse_links": 1
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
            if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                chat_id = event.chat_id
                message = event.obj['message']
                # text = message['text']
                # payload = json.loads(event.object.payload)
                text = event.object.message['text']
                user_id = event.object.message['from_id']
                message_id = event.object.message['conversation_message_id']

                if chat_id == CONST and text == "enter":
                    pass

                elif chat_id == CONST and text == "reenter":
                    pass

                elif chat_id == CONST and text == "exit":
                    pass

                elif str(user_id) in DEV and text == "add_buttons":
                    keyboard = VkKeyboard(inline=False, one_time=False)
                    keyboard.add_button(
                        label="Зашёл",
                        color=VkKeyboardColor.POSITIVE,
                        payload={"command": "enter"}
                    )
                    keyboard.add_button(
                        label="Перезахожу",
                        color=VkKeyboardColor.PRIMARY,
                        payload={"command": "reenter"}
                    )
                    keyboard.add_button(
                        label="Вышел",
                        color=VkKeyboardColor.NEGATIVE,
                        payload={"command": "exit"}
                    )

                    vk_session.method("messages.send", {
                        "chat_id": chat_id,
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
