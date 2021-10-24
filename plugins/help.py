from pyrogram import Client, Filters


@Client.on_message(Filters.command(["help"]))
async def start(client, message):
    helptxt = f"Hello again. If you want to download any video from YouTube, you should send link that video.\n Then you can receive your video by this bot.\n Link of owner this bot👨‍💻: @Boburjon_Ravzatov"
    await message.reply_text(helptxt)