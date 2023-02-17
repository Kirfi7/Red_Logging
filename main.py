import vk_api
import json
import asyncio

from db_func import *
from table_pars import reset_table
from cfg import TOKEN, DEV, CONST, PREFIX
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

vk_session = vk_api.VkApi(token=TOKEN)
lp = VkBotLongPoll(vk_session, 218860473)
vk = vk_session.get_api()

async def reset_table_and_sender():
    reset_table()
    await sender(CONST, f"База данных обновлена")

async def relog_server():
    await sender(CONST, f"🔄 {nick} перезаходит на сервер!\n\n{get_online()}")

async def go_out_server():
    await sender(CONST, f"⏹ {nick} вышел с сервера!\n\n{get_online()}")

async def go_to_server():
    await sender(CONST, f"▶️ {nick} зашёл на сервер!\n\n{get_online()}")

async def error():
    await sender(CONST, f"{to_id}!")

async def on_server():
    await sender(CONST, f"[id{to_id}|Пользователь] теперь {is_online}")

async def sender(for_chat_id, message_text):
    await vk_session.method("messages.send", {
        "chat_id": for_chat_id,
        "message": message_text,
        "random_id": 0,
    })


while True:
    try:
        for event in lp.listen():
            if event.type == VkBotEventType.MESSAGE_EVENT:

                admin_id = event.obj['user_id']
                nick = get_nick(admin_id)

                if "re" in event.object.payload.get('call_back'):
                    if online(admin_id) == 1:
                        asyncio.get_event_loop().run_until_complete(relog_server())
                    else:
                        vk.messages.sendMessageEventAnswer(
                            event_id=event.object.event_id,
                            user_id=event.object.user_id,
                            peer_id=event.object.peer_id,
                            event_data=json.dumps({"type": "show_snackbar", "text": "Ошибка, вы ещё не на сервере!"}))

                elif "dis" in event.object.payload.get('call_back'):
                    if online(admin_id) == 1:
                        del_online(admin_id)
                        asyncio.get_event_loop().run_until_complete(go_out_server())
                    else:
                        vk.messages.sendMessageEventAnswer(
                            event_id=event.object.event_id,
                            user_id=event.object.user_id,
                            peer_id=event.object.peer_id,
                            event_data=json.dumps({"type": "show_snackbar", "text": "Ошибка, вы ещё не на сервере!"}))

                elif "co" in event.object.payload.get('call_back'):
                    if online(admin_id) == 0:
                        add_online(admin_id)
                        asyncio.get_event_loop().run_until_complete(go_to_server())
                    else:
                        vk.messages.sendMessageEventAnswer(
                            event_id=event.object.event_id,
                            user_id=event.object.user_id,
                            peer_id=event.object.peer_id,
                            event_data=json.dumps({"type": "show_snackbar", "text": "Ошибка, вы уже на сервере!"}))

            if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.chat_id == CONST:

                text = event.object.message['text']
                user_id = event.object.message['from_id']

                if text[0] in PREFIX and str(user_id) in DEV:
                    cmd = text[1:]

                    if cmd == "change":
                        to_id = get_to(event.object.message)

                        if to_id == 0:
                            asyncio.get_event_loop().run_until_complete(error())

                        else:
                            changed_online = change_online(to_id)
                            is_online = "онлайн" if changed_online == 1 else "оффлайн"
                            asyncio.get_event_loop().run_until_complete(on_server())

                    elif cmd == "reset":
                        keyboard = VkKeyboard(inline=False, one_time=False)
                        keyboard.add_callback_button(
                            label="Зашёл",
                            color=VkKeyboardColor.POSITIVE,
                            payload={
                                "call_back": "co"
                            }
                        )
                        keyboard.add_callback_button(
                            label="Перезахожу",
                            color=VkKeyboardColor.PRIMARY,
                            payload={"call_back": "re"},
                        )
                        keyboard.add_callback_button(
                            label="Вышел",
                            color=VkKeyboardColor.NEGATIVE,
                            payload={"call_back": "dis"}
                        )

                        vk_session.method("messages.send", {
                            "chat_id": CONST,
                            "message": "Секунду...",
                            "keyboard": keyboard.get_empty_keyboard(),
                            "random_id": 0
                        })
                        vk_session.method("messages.send", {
                            "chat_id": CONST,
                            "message": "Обновление БД...",
                            "keyboard": keyboard.get_keyboard(),
                            "random_id": 0
                        })

                        asyncio.get_event_loop().run_until_complete(reset_table_and_sender())
                        # asyncio.run(reset_table_and_sender())

    except Exception as error:
        print(error)
