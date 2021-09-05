# import os
# import asyncio
from pyrogram.errors import YouBlockedUser, BadRequest
from userge import Config, Message, userge
from userge.utils.exceptions import StopConversation
from userge.utils import get_file_id

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
        async with userge.conversation("notemusicbot") as conv:
            await conv.send_message("/start")
            k = await conc.get_response(mark_read=True)
            await conv.send_message(f"/music {song}")
            await message.reply(k)
            try:
                async for msg in await userge.search_message("notemusicbot", f"{song}", limit=1, filter=audio):
                    f_id = get_file_id(msg)
            except:
                await message.err("Encontrei foi nada...")
            if not f_id:
                await message.edit("Credita que não encontrei nada.")
                return
            await userge.send_audio(message.chat.id, f_id)
            await message.delete()
    except YouBlockedUser:
        await message.edit("Desbloqueie o **@notemusicbot**")
    except StopConversation:
        await message.err("O Bot está morto...")
    