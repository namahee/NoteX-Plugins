""" NoteX/Samuca @samuca78 Snooze """

import asyncio

from userge import Message, userge


@userge.on_cmd(
    "fui$",
    about={
        "header": "executa .afk",
        "flags": {
            "-s": "Sleeping",
            "-b": "Busy",
            "-w": "Watching",
        },
    },
    trigger="",
    allow_via_bot=False,
)
async def fui_(message: Message):
    """fui_"""
    _fui = "!afk Zzz... | https://telegra.ph/file/5f5ef5dde5e811ab753b5.gif"
    await message.try_to_edit(_fui, del_in=1)


async def check_and_send(message: Message, *args, **kwargs):
    replied = message.reply_to_message
    if replied:
        await asyncio.gather(message.delete(), replied.reply(*args, **kwargs))
    else:
        await message.edit(*args, **kwargs)
