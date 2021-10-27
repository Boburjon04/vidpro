from pyrogram import Client, Filters, StopPropagation, InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(Filters.command(["start"]), group=-2)
async def start(client, message):
    # return
    joinButton = InlineKeyboardMarkup([
        [InlineKeyboardButton("Bizning kanal🛰", url="https://t.me/BoburjonVlogs")],
        [InlineKeyboardButton(
            "Bot yaratuvchisi👨‍💻", url="https://t.me/Boburjon_Ravzatov")]
    ])
    welcomed = f"Assalomu alaykum! <b>{message.from_user.first_name}</b>\nBu bot sizga YouTube dagi videolarni telegramga yuklab berishga xizmat qiladi🎞\nShunchaki YouTube dagi video sillkasi(link)ini botga yuboring, video formatlarini tanlang va video sizga yuboriladi📥\nBatafsil ma'lumot uchun /help buyrug'ini yuboring!"
    await message.reply_text(welcomed, reply_markup=joinButton)
    raise StopPropagation