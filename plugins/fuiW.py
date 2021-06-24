import asyncio

from userge import Message, userge

import random


# Watching
wt = (
    "I'm watching.",
    "Watching.",
    "I'm watching right now.",
)
WTlink = (
    "https://telegra.ph/file/5f153409f120195f14491.gif",
    "https://telegra.ph/file/081808e86849851e6510c.gif",
    "https://telegra.ph/file/d923af73a7e7643e6d902.gif",
)


@userge.on_cmd(
    "Fui -w$",
    about={
        "header": "plugin",
    },
    trigger="",
    allow_via_bot=False,
)
async def _fui(message: Message):
    fui_ = f"!afk {random.choice(wt)} | {random.choice(WTlink)}"
    await message.try_to_edit(fui_, del_in=1)

async def check_and_send(message: Message, *args, **kwargs):
    replied = message.reply_to_message
    if replied:
        await asyncio.gather(message.delete(), replied.reply(*args, **kwargs))
    else:
        await message.edit(*args, **kwargs)
