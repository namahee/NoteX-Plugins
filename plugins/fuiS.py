import asyncio

from userge import Message, userge

import random


# Sleeping
sp = (
    "I'm sleeping.",
    "Sleeping.",
    "Zzz...",
)
SPlink = (
    "https://telegra.ph/file/ca7449b0175e38aa91173.gif",
    "https://telegra.ph/file/e24024983e40d14e6ba7c.gif",
    "https://telegra.ph/file/95d666e5638d30574688f.gif",
    "https://telegra.ph/file/17b67e992945d187c15f8.gif",
)


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