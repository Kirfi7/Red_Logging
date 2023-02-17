import vk_api


TOKEN = "vk1.a.y7jZVoqd0_HqNWZTEzS6hLwEp9Rb9Yu5I7DPc7hWXk5UB5qP7d9bpIFZVBJL6iaAcsvS5xKAN5CnQYSNXX89TBXCuK7cS1NOfnMePmQ6-d5dmtDz_rGRq4K4DtrImAUvSqdoopX_7Hs4Rq2fZx1-PR1GMN_hwos5VgKUgVcPeoU1x_0dtsj65oBp9U_NuYAnbogGdMdUS-Fy-Tzr0p4OCg"

DEV = ["534422651", "468509613"]

PREFIX = ["/", "!", "+"]

CONST = 2

vk_session = vk_api.VkApi(token=TOKEN)


def chat_sender(for_chat_id, message_text):
    vk_session.method("messages.send", {
        "chat_id": for_chat_id,
        "message": message_text,
        "random_id": 0
    })
