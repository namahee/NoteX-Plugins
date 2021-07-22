from userge import Message, userge, Config

@userge.on_cmd("get_kek", about={"header": "nothing"})
async def get_kek(message: MMessage:
    await message.edit(Config.HEROKU_API_KEY