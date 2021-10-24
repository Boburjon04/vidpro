from pyrogram import Client, Filters, StopPropagation, InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(Filters.command(["start"]), group=-2)
async def start(client, message):
    # return
    joinButton = InlineKeyboardMarkup([
        [InlineKeyboardButton("Our Channel", url="https://t.me/BoburjonVlogs")],
        [InlineKeyboardButton(
            "Owner of the Bot", url="https://t.me/Boburjon_Ravzatov")]
    ])
    welcomed = f"Hello <b>{message.from_user.first_name}</b>\n This bot helps you for downloading videos from YouTube\nJust send any YouTube video link and get your video file\n/help for More info"
    await message.reply_text(welcomed, reply_markup=joinButton)
    raise StopPropagation