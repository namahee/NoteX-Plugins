""" NoteX/Samuca @samuca78 Snooze """

import asyncio

from userge import Message, userge

import random


# Reasons/Status

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
    "Fui$",
    about={
        "header": "executa .afk",
        "flags": {
            "-s": "Sleeping",
            "-b": "Busy",
            "-w": "Watching",
        },
    },
)
async def fui(message: Message):
    pass

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
