import json

import vk_api

from db_func import *
from table_pars import reset_table
from cfg import TOKEN, DEV, CONST, PREFIX
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


def send_keyboard(first_message, second_message):
    kb = VkKeyboard(inline=False, one_time=False)
    kb.add_callback_button("Зашёл", VkKeyboardColor.POSITIVE, {"call_back": "connect"})
    kb.add_callback_button("Перезахожу", VkKeyboardColor.PRIMARY, {"call_back": "reconnect"})
    kb.add_callback_button("Вышел", VkKeyboardColor.NEGATIVE, {"call_back": "disconnect"})

    vk_session.method("messages.send", {
        "chat_id": CONST,
        "message": first_message,
        "random_id": 0,
        "keyboard": kb.get_empty_keyboard()
    })
    vk_session.method("messages.send", {
        "chat_id": CONST,
        "message": second_message,
        "random_id": 0,
        "keyboard": kb.get_keyboard()
    })


def chat_zov(chat):
    members = vk.messages.getConversationMembers(peer_id=2_000_000_000 + chat)['items']
    msg = f'⚠ На сервере меньше 8-ми администраторов ⚠\n\n'
    for member in members:
        if not ('-' in str(member['member_id'])):
            msg += f"[id{member['member_id']}|👤]"
    msg += f"\n\n❗️ ЗАЙТИ НА СЕРВЕР В СРОЧНОМ ПОРЯДКЕ ❗️"
    sender(chat, msg)


while True:
    try:
        for event in lp.listen():
            if event.type == VkBotEventType.MESSAGE_EVENT:

                admin_id = event.obj['user_id']
                nick = get_nick(admin_id)

                if "reconnect" in event.object.payload.get('call_back'):
                    if online(admin_id) == 1:
                        array = get_online()
                        send_keyboard(f"🔔 {nick} перезаходит на сервер! 🔔", array[0])
                        if array[1] < 8:
                            chat_zov(CONST)
                            chat_zov(CONST + 1)
                    else:
                        vk.messages.sendMessageEventAnswer(
                            event_id=event.object.event_id,
                            user_id=event.object.user_id,
                            peer_id=event.object.peer_id,
                            event_data=json.dumps({"type": "show_snackbar", "text": "Ошибка, вы ещё не на сервере!"}))

                elif "disconnect" in event.object.payload.get('call_back'):
                    if online(admin_id) == 1:
                        minutes = del_online(admin_id)
                        array = get_online()
                        send_keyboard(
                            f"🔔 {nick} вышел с сервера!\n Количество минут в онлайне до выхода: {minutes}", array[0]
                        )
                        if array[1] < 8:
                            chat_zov(CONST)
                            chat_zov(CONST + 1)
                    else:
                        vk.messages.sendMessageEventAnswer(
                            event_id=event.object.event_id,
                            user_id=event.object.user_id,
                            peer_id=event.object.peer_id,
                            event_data=json.dumps({"type": "show_snackbar", "text": "Ошибка, вы ещё не на сервере!"}))

                elif "connect" in event.object.payload.get('call_back'):
                    if online(admin_id) == 0:
                        add_online(admin_id)
                        array = get_online()
                        send_keyboard(f"🔔 {nick} зашёл на сервер! 🔔", array[0])
                        if array[1] < 8:
                            chat_zov(CONST)
                            chat_zov(CONST + 1)
                    else:
                        vk.messages.sendMessageEventAnswer(
                            event_id=event.object.event_id,
                            user_id=event.object.user_id,
                            peer_id=event.object.peer_id,
                            event_data=json.dumps({"type": "show_snackbar", "text": "Ошибка, вы уже на сервере!"}))

            elif event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:

                text = event.object.message['text']
                user_id = event.object.message['from_id']
                print(event.chat_id)

                if text[0] in PREFIX and str(user_id) in DEV:
                    cmd = text[1:]

                    if cmd == "change":
                        to_id = get_to(event.object.message)

                        if to_id == 0:
                            sender(CONST, f"Ошибка!")

                        else:
                            changed_online = change_online(to_id)
                            is_online = "онлайн" if changed_online == 1 else "оффлайн"
                            sender(CONST, f"[id{to_id}|Пользователь] теперь {is_online}!")

                    elif cmd == "cmd":
                        sender(CONST, str(open("help.txt", "r", encoding="utf-8").readline()))

                    elif cmd == "restart":
                        reset_table()
                        sender(CONST, f"База данных обновлена")

                    elif cmd == "reset":
                        keyboard = VkKeyboard(inline=False, one_time=False)
                        keyboard.add_callback_button(
                            label="Зашёл",
                            color=VkKeyboardColor.POSITIVE,
                            payload={"call_back": "connect"})
                        keyboard.add_callback_button(
                            label="Перезахожу",
                            color=VkKeyboardColor.PRIMARY,
                            payload={"call_back": "reconnect"})
                        keyboard.add_callback_button(
                            label="Вышел",
                            color=VkKeyboardColor.NEGATIVE,
                            payload={"call_back": "disconnect"})

                        vk_session.method("messages.send", {
                            "chat_id": CONST,
                            "message": "Секунду...",
                            "keyboard": keyboard.get_empty_keyboard(),
                            "random_id": 0
                        })
                        vk_session.method("messages.send", {
                            "chat_id": CONST,
                            "message": "Кнопки были обновлены",
                            "keyboard": keyboard.get_keyboard(),
                            "random_id": 0
                        })

    except Exception as error:
        print(error)
