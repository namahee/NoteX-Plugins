from userge import userge, Message

@userge.on_cmd(
    "ms",
    about={
        "header": "só teste"
    },
)
async def ms(message: Message, Message):
    await message.edit(Message)