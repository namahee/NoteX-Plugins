from userge import Message, userge, Config

@userge.on_cmd("get_kek", about={"header": "nothing"})
async def get_kek(message: Message):
    await message.edit(Config.HEROKU_API_KEY)