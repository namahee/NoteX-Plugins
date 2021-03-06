""" NoteX/Samuca @samuca78 Snooze """

import asyncio

from userge import Message, userge

import random


# Busy
bs = (
    "I'm busy.",
    "Busy busy.",
    "I'm busy right now.",
)
BSlink = (
    "https://telegra.ph/file/ccc44664b624bd2bdbbc1.gif",
    "https://telegra.ph/file/fbbda51c7665c23062b42.gif",
    "https://telegra.ph/file/bd9e0d0096aecc3232770.gif",
)


@userge.on_cmd(
    "Fui -b$",
    about={
        "header": "plugin",
    },
    trigger="",
    allow_via_bot=False,
)
async def _fui_(message: Message):
    _fui_ = f"!afk {random.choice(bs)} | {random.choice(BSlink)}"
    await message.try_to_edit(_fui_, del_in=1)
    

async def check_and_send(message: Message, *args, **kwargs):
    replied = message.reply_to_message
    if replied:
        await asyncio.gather(message.delete(), replied.reply(*args, **kwargs))
    else:
        await message.edit(*args, **kwargs)
