from pyrogram import Client, Filters


@Client.on_message(Filters.command(["help"]))
async def start(client, message):
    helptxt = f"🚩 Botning Yordam olish bo'limiga xush kelibsiz.\n🚩Agar siz YouTube dan o'zingizga yoqqan videoni telegramdan yuklab olmoqchi bo'lsangiz o'sha videoni faqatgina sillkasini(link)ini yuboring(Sarlavhasi bilan emas faqat linkini).\n🚩 Keyin videoni o'zingizga qulay bo'lgan formatini tanlang va bot sizga videoni bir necha daqiqa ichida sizga yuboradi.\n🚩 Agarda sizda bot yuzasidan qandaydir savol yoki taklifingiz bo'lsa, bot yaratuvchisiga murojaat qiling.\n🚩 Bot yaratuvchisi lichkasi👨‍💻: @Boburjon_Ravzatov\n🚩 Kanalimiz: @BoburjonVlogs"
    await message.reply_text(helptxt)