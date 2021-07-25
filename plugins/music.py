# import os
# import asyncio
from pyrogram.errors import YouBlockedUser
from userge import Config, Message, userge
from userge.utils.exceptions import StopConverimport

@userge.on_cmd(
    "song",
    about={
        "header": "Plugin de música",
        "como usar": "{tr}song `Haddaway - What is Love?`",
    },
    allow_via_bot=False,
    allow_channels=False,
)
async def _song(message: Message):
    song = message.input_str
    if not song:
        await message.err("Escreva alguma música após o comando.")
        return
    try:
        async with userge.conversation("NoteMusic_bot") as conv:
            await conv.send_message("/start")
            await conc.get_response(mark_read=True)
            await conv.send_messsong(f"/music {song}")
            await userge.search_message(f"{song}")
            
    except YouBlockedUser:
        await message.edit("Desbloqueie o **@NoteMusic_bot**")
    except StopConversation:
        await message.err("O Bot está morto...")
    