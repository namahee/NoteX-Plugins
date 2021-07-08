""" Módulo de testes para o @NoteZV com fins de aprendizado """

import asyncio
import os
from pyrogram.errors import YouBlockedUser
from userge import Config, Message, userge
from userge.utils.exceptions import StopConversation

@userge.on_cmd(
    "nbot",
    about={
        "header": "criar um bot",
        "como usar": "{tr}nbot [nome] | [username_bot] or [usernameBot]", 
    },
    allow_via_bot=False,
    allow_channels=False,
)
async def nbot_(message: Message):
    name = message.input_str.split(" | ", maxsplit=1)
    if not name:
        await message.err("Coloque um nome e um username.")
        return
    try:
        async with userge.conversation("BotFather") as conv:
            await conv.send_message("/start")
            await conv.get_response(mark_read=True)
            await conv.send_message("/newbot")
            await conv.send_message(name[0])
            await conv.send_message(name[1])
            
        await message.edit(f"Prontinho, bot criado. [Aqui](t.me/{name[1})")
    except YouBlockedUser:
        await message.edit("Desbloqueie o **@BotFather**")
    except StopConversation:
        await msg.err("O Bot está morto...")