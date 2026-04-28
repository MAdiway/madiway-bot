@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    is_admin = user_id in ADMINS
    
    # Siz bergan andoza asosida matn
    status_icon = "🛡 **Siz tizimda: Adminsiz** ✅" if is_admin else "👤 **Siz tizimda: Foydalanuvchisiz**"
    
    desc = (
        "🏔 **MadiWay | Global Logistics & Dispatch** 🚀\n\n"
        "Xalqaro yuk tashish va professional dispetcherlik xizmatlari tarmog'iga xush kelibsiz!\n"
        "Biz to'rtta davlatni yagona xavfsiz marshrut bilan bog'laymiz:\n\n"
        "🌍 **Bizning yo'nalishlar:**\n"
        "📍 O'zbekiston 🇺🇿\n"
        "📍 Qozog'iston 🇰🇿\n"
        "📍 Rossiya 🇷🇺\n"
        "📍 Ozarbayjon 🇦🇿\n\n"
        f"{status_icon}\n\n"
        "✅ Ishonchlilik: Yukingiz manzili va vaqti bizning nazoratimizda.\n"
        "✅ Tezkorlik: Eng qulay va xavfsiz yo'llarni taqdim etamiz.\n"
        "✅ Professional Dispetcherlik: 24/7 aloqa va harakat nazorati.\n\n"
        "🚛 **MadiWay — Sizning yukingiz, bizning mas'uliyatimiz!**\n\n"
        "📥 Bog'lanish uchun: [@Madiways]\n"
        "link: T.me/MADIWAYy"
    )
    
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    # Ilova tugmasi
    kb.add(KeyboardButton("🏔 MadiWay Ilovasi", web_app=WebAppInfo(url=WEB_APP_URL)))
    
    # Adminlar uchun qo'shimcha Kanal tugmasi
    if is_admin:
        kb.add(KeyboardButton("🔗 Kanalga o'tish"))
        
    await message.answer(desc, parse_mode="Markdown", reply_markup=kb)
