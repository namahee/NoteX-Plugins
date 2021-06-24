import asyncio

from userge import Message, userge

import random


@userge.on_cmd(
    "Fui -s$",
    about={
        "header": "plugin",
    },
    trigger="",
    allow_via_bot=False,
)
async def fui_(message: Message):
    """ Executa .afk """
    _fui = f"!afk {random.choice(sp)} | {random.choice(SPlink)}"
    await message.try_to_edit(_fui, del_in=1)
    
async def check_and_send(message: Message, *args, **kwargs):
    replied = message.reply_to_message
    if replied:
        await asyncio.gather(message.delete(), replied.reply(*args, **kwargs))
    else:
        await message.edit(*args, **kwargs)