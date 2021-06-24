""" setup AFK mode """

import asyncio
import time
from random import randint
from re import compile as comp_regex

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from userge import Config, Message, filters, get_collection, userge
from userge.utils import time_formatter

_TELE_REGEX = comp_regex(
    r"http[s]?://(i\.imgur\.com|telegra\.ph/file|t\.me)/(\w+)(?:\.|/)(gif|jpg|png|jpeg|[0-9]+)(?:/([0-9]+))?"
)

CHANNEL = userge.getCLogger(__name__)
SAVED_SETTINGS = get_collection("CONFIGS")
AFK_COLLECTION = get_collection("AFK")

IS_AFK = False
IS_AFK_FILTER = filters.create(lambda _, __, ___: bool(IS_AFK))
REASON = ""
TIME = 0.0
USERS = {}


async def _init() -> None:
    global IS_AFK, REASON, TIME  # pylint: disable=global-statement
    data = await SAVED_SETTINGS.find_one({"_id": "AFK"})
    if data:
        IS_AFK = data["on"]
        REASON = data["data"]
        TIME = data["time"] if "time" in data else 0
    async for _user in AFK_COLLECTION.find():
        USERS.update({_user["_id"]: [_user["pcount"], _user["gcount"], _user["men"]]})


@userge.on_cmd(
    "afk",
    about={
        "header": "Set to AFK mode",
        "description": "Sets your status as AFK. Responds to anyone who tags/PM's.\n"
        "you telling you are AFK. Switches off AFK when you type back anything.",
        "usage": "{tr}afk or {tr}afk [reason]",
    },
    allow_channels=False,
)
async def active_afk(message: Message) -> None:
    """turn on or off afk mode"""
    global REASON, IS_AFK, TIME  # pylint: disable=global-statement
    IS_AFK = True
    TIME = time.time()
    REASON = message.input_str
    match_ = _TELE_REGEX.search(REASON)
    if match_:
        r_ = REASON.split(" | ", maxsplit=1)
        STATUS_ = r_[0]
        await asyncio.gather(
            CHANNEL.log(f"You went AFK! : `{STATUS_}` [\u200c]({match_.group(0)})"),
            message.edit("`You went AFK!`", del_in=1),
            AFK_COLLECTION.drop(),
            SAVED_SETTINGS.update_one(
                {"_id": "AFK"},
                {"$set": {"on": True, "data": STATUS_, "time": TIME}},
                upsert=True,
            ),
        )
    else:
        await asyncio.gather(
            CHANNEL.log(f"You went AFK! : `{REASON}`"),
            message.edit("`You went AFK!`", del_in=1),
            AFK_COLLECTION.drop(),
            SAVED_SETTINGS.update_one(
                {"_id": "AFK"},
                {"set": {"on": True, "data": REASON, "time": TIME}},
                upsert=True,
            ),
        )


@userge.on_filters(
    IS_AFK_FILTER
    & ~filters.me
    & ~filters.bot
    & ~filters.user(Config.TG_IDS)
    & ~filters.edited
    & (
        filters.mentioned
        | (
            filters.private
            & ~filters.service
            & (
                filters.create(lambda _, __, ___: Config.ALLOW_ALL_PMS)
                | Config.ALLOWED_CHATS
            )
        )
    ),
    allow_via_bot=False,
)
async def handle_afk_incomming(message: Message) -> None:
    """handle incomming messages when you afk"""
    if not message.from_user:
        return
    user_id = message.from_user.id
    chat = message.chat
    user_dict = await message.client.get_user_dict(user_id)
    afk_time = time_formatter(round(time.time() - TIME))
    coro_list = []

    message.client
    chat_id = message.chat.id
    if user_id in USERS:
        if not (USERS[user_id][0] + USERS[user_id][1]) % randint(2, 4):
            match = _TELE_REGEX.search(REASON)
            if match:
                r = REASON.split(" | ", maxsplit=1)
                STATUS = r[0]
                out_str = (
                    f"⚡️ **Auto Reply** ⒶⒻⓀ \n🕑 **Last Seen:** {afk_time} ago\n"
                    f"▫️ **Status**: {STATUS}"
                )
                coro_list.append(
                    await chat_id.send_animation(
                        chat_id,
                        animation=match.group(0),
                        caption=out_str,
                        reply_markup=_afk_.afk_buttons(),
                    )
                )
            else:
                out_str = (
                    f"⚡️ **Auto Reply** ⒶⒻⓀ \n🕑 **Last Seen:** {afk_time} ago\n"
                    f"▫️ **Status**: {REASON}"
                )
                coro_list.append(message.reply(out_str))
        if chat.type == "private":
            USERS[user_id][0] += 1
        else:
            USERS[user_id][1] += 1
    else:
        match = _TELE_REGEX.search(REASON)
        if match:
            match.group(0)
            r = REASON.split(" | ", maxsplit=1)
            STATUS = r[0]
            out_str = (
                f"⚡️ **Auto Reply** ⒶⒻⓀ \n🕑 **Last Seen:** {afk_time} ago\n"
                f"▫️ **Status**: {STATUS}"
            )
            await send_animation(
                chat_id,
                animation=match.group(0),
                caption=out_str,
                reply_markup=_afk_.afk_buttons(),
            )
            # url_ = LINK.strip()
            # type_, media_ = await _afk_.check_media_link(LINK)
            # if type_ == "url_gif":
            # await client.send_animation(
            # chat_id,
            # animation=url_,
            # caption=out_str,
            # reply_markup=_afk_.afk_buttons(),
            # )
            # elif type_ == "url_image":
            # await client.send_photo(
            # chat_id,
            # photo=url_,
            # caption=out_str,
            # reply_markup=_afk_.afk_buttons(),
            # )
        else:
            out_str = (
                f"⚡️ **Auto Reply** ⒶⒻⓀ \n🕑 **Last Seen:** {afk_time} ago\n"
                f"▫️ **Status**: {REASON}"
            )
            coro_list.append(message.reply(out_str))
        if chat.type == "private":
            USERS[user_id] = [1, 0, user_dict["mention"]]
        else:
            USERS[user_id] = [0, 1, user_dict["mention"]]
    if chat.type == "private":
        coro_list.append(
            CHANNEL.log(
                f"#PRIVATE\n{user_dict['mention']} send you\n\n" f"{message.text}"
            )
        )
    else:
        coro_list.append(
            CHANNEL.log(
                "#GROUP\n"
                f"{user_dict['mention']} tagged you in [{chat.title}](http://t.me/{chat.username})\n\n"
                f"{message.text}\n\n"
                f"[goto_msg](https://t.me/c/{str(chat.id)[4:]}/{message.message_id})"
            )
        )
    coro_list.append(
        AFK_COLLECTION.update_one(
            {"_id": user_id},
            {
                "$set": {
                    "pcount": USERS[user_id][0],
                    "gcount": USERS[user_id][1],
                    "men": USERS[user_id][2],
                }
            },
            upsert=True,
        )
    )
    await asyncio.gather(*coro_list)


class _afk_:
    async def check_media_link(media_link: str):
        match_ = _TELE_REGEX.search(media_link.strip())
        if not match_:
            return None, None
        if match_.group(1) == "i.imgur.com":
            link = match_.group(0)
            link_type = "url_gif" if match_.group(3) == "gif" else "url_image"
        elif match_.group(1) == "telegra.ph/file":
            link = match_.group(0)
            link_type = "url_image"
        else:
            link_type = "tg_media"
            if match_.group(2) == "c":
                chat_id = int("-100" + str(match_.group(3)))
                message_id = match_.group(4)
            else:
                chat_id = match_.group(2)
                message_id = match_.group(3)
            link = [chat_id, int(message_id)]
        return link_type, link

    def afk_buttons() -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(text="REPO", url=Config.UPSTREAM_REPO),
            ]
        ]
        return InlineKeyboardMarkup(buttons)


@userge.on_filters(IS_AFK_FILTER & filters.outgoing, group=-1, allow_via_bot=False)
async def handle_afk_outgoing(message: Message) -> None:
    """handle outgoing messages when you afk"""
    global IS_AFK  # pylint: disable=global-statement
    IS_AFK = False
    afk_time = time_formatter(round(time.time() - TIME))
    replied: Message = await message.reply("`I'm no longer AFK!`", log=__name__)
    coro_list = []
    if USERS:
        p_msg = ""
        g_msg = ""
        p_count = 0
        g_count = 0
        for pcount, gcount, men in USERS.values():
            if pcount:
                p_msg += f"👤 {men} ✉️ **{pcount}**\n"
                p_count += pcount
            if gcount:
                g_msg += f"👥 {men} ✉️ **{gcount}**\n"
                g_count += gcount
        coro_list.append(
            replied.edit(
                f"`You recieved {p_count + g_count} messages while you were away. "
                f"Check log for more details.`\n\n**AFK time** : __{afk_time}__",
                del_in=3,
            )
        )
        out_str = (
            f"You've recieved **{p_count + g_count}** messages "
            + f"from **{len(USERS)}** users while you were away!\n\n**AFK time** : __{afk_time}__\n"
        )
        if p_count:
            out_str += f"\n**{p_count} Private Messages:**\n\n{p_msg}"
        if g_count:
            out_str += f"\n**{g_count} Group Messages:**\n\n{g_msg}"
        coro_list.append(CHANNEL.log(out_str))
        USERS.clear()
    else:
        await asyncio.sleep(3)
        coro_list.append(replied.delete())
    coro_list.append(
        asyncio.gather(
            AFK_COLLECTION.drop(),
            SAVED_SETTINGS.update_one(
                {"_id": "AFK"}, {"$set": {"on": False}}, upsert=True
            ),
        )
    )
    await asyncio.gather(*coro_list)


AFK_REASONS = (
    "I'm busy right now. Please talk in a bag and when I come back you can just give me the bag!",
    "I'm away right now. If you need anything, leave a message after the beep: \
`beeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeep!`",
    "You missed me, next time aim better.",
    "I'll be back in a few minutes and if I'm not...,\nwait longer.",
    "I'm not here right now, so I'm probably somewhere else.",
    "Roses are red,\nViolets are blue,\nLeave me a message,\nAnd I'll get back to you.",
    "Sometimes the best things in life are worth waiting for…\nI'll be right back.",
    "I'll be right back,\nbut if I'm not right back,\nI'll be back later.",
    "If you haven't figured it out already,\nI'm not here.",
    "I'm away over 7 seas and 7 countries,\n7 waters and 7 continents,\n7 mountains and 7 hills,\
7 plains and 7 mounds,\n7 pools and 7 lakes,\n7 springs and 7 meadows,\
7 cities and 7 neighborhoods,\n7 blocks and 7 houses...\
    Where not even your messages can reach me!",
    "I'm away from the keyboard at the moment, but if you'll scream loud enough at your screen,\
    I might just hear you.",
    "I went that way\n>>>>>",
    "I went this way\n<<<<<",
    "Please leave a message and make me feel even more important than I already am.",
    "If I were here,\nI'd tell you where I am.\n\nBut I'm not,\nso ask me when I return...",
    "I am away!\nI don't know when I'll be back!\nHopefully a few minutes from now!",
    "I'm not available right now so please leave your name, number, \
    and address and I will stalk you later. :P",
    "Sorry, I'm not here right now.\nFeel free to talk to my userbot as long as you like.\
I'll get back to you later.",
    "I bet you were expecting an away message!",
    "Life is so short, there are so many things to do...\nI'm away doing one of them..",
    "I am not here right now...\nbut if I was...\n\nwouldn't that be awesome?",
)
