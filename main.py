import logging
import json
import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# --- KONFIGURATSIYA ---
TOKEN = "8791239714:AAGeDUktKzciq9ftUp4lZZOzIuyItQXv5wM"
GROUP_ID = -1003996104316
CHANNEL_ID = "@MADIWAYy"
# Siz yuborgan yangi banner rasm manzili
BANNER_URL = "https://raw.githubusercontent.com/madiway/madiway-bot/main/madiway_banner.png"
WEB_APP_URL = "https://madiway.github.io/madiway-bot/"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# So'kinishlar ro'yxati (Siz bergan variant)
BAD_WORDS = [
    "sokish1", "sokish2", "jalab", "skachat", "qo'toq", "am", "qotoq", "shalpang", 
    "iflos", "yaramas", "itdan tarqagan", "dalbayob", "axmoq", "onangni", "otangni", 
    "gey", "pider", "gandon", "lox", "tovuqmiya", "manqurt", "qaltis", "beshaka"
]

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    # Faqat bitta tugma: Ilovaga kirish
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="🚛 Ilovaga kirish", web_app=WebAppInfo(url=WEB_APP_URL)))
    
    # Siz bergan aniq matn
    caption = (
        "🏔 **MadiWay | Global Logistics & Dispatch 🚀**\n\n"
        "Xalqaro yuk tashish va professional dispetcherlik xizmatlari tarmog'iga xush kelibsiz! "
        "Biz to'rtta davlatni yagona xavfsiz marshrut bilan bog'laymiz:\n\n"
        "🌍 **Bizning yo'nalishlar:**\n"
        "📍 O'zbekiston 🇺🇿\n"
        "📍 Qozog'iston 🇰🇿\n"
        "📍 Rossiya 🇷🇺\n"
        "📍 Ozarbayjon 🇦🇿\n\n"
        "🛡 **Nega aynan MadiWay?**\n"
        "✅ Ishonchlilik: Yukingiz manzili va vaqti bizning nazoratimizda.\n"
        "✅ Tezkorlik: Eng qulay va xavfsiz yo'llarni taqdim etamiz.\n"
        "✅ Professional Dispetcherlik: 24/7 aloqa va harakat nazorati.\n\n"
        "🚛 **MadiWay — Sizning yukingiz, bizning mas'uliyatimiz!**\n\n"
        "📥 Bog'lanish uchun: [@Madiways]\n"
        "🔗 Kanal: T.me/MADIWAYy\n"
        "🤖 Bot: @MADIWAYy_bot\n"
        "👥 Gruppa: @MADIWAY_Gr"
    )
    
    try:
        # Rasmni yuborish (Siz bergan banner bilan)
        await bot.send_photo(
            chat_id=message.chat.id, 
            photo=BANNER_URL, 
            caption=caption, 
            reply_markup=kb, 
            parse_mode="Markdown"
        )
    except Exception as e:
        # Rasmda xato bo'lsa, matn o'zi chiqadi (Tugma bilan birga)
        logging.error(f"Start xatosi: {e}")
        await message.answer(caption, reply_markup=kb, parse_mode="Markdown")

# --- WEB APP MA'LUMOTLARINI QABUL QILISH ---
@dp.message_handler(content_types=['web_app_data'])
async def web_app_data_handler(message: types.Message):
    data = json.loads(message.web_app_data.data)
    now = datetime.datetime.now().strftime("%d.%m.%Y | %H:%M")
    
    text = (
        f"🚛 **YANGI YUK E'LONI**\n\n"
        f"📍 Yo'nalish: #{data['t_name']}\n"
        f"📦 Tavsif: {data['desc']}\n"
        f"⏰ Vaqt: {data['time']}\n"
        f"👤 Yuboruvchi: {data['u_name']}\n"
        f"📅 Sana: {now}"
    )

    # Kanal uchun tugmalar
    kb = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("🤖 Bot", url="https://t.me/MADIWAYy_bot"),
        InlineKeyboardButton("📩 Lichka", url=f"tg://user?id={message.from_user.id}"),
        InlineKeyboardButton("📞 Raqam", callback_data=f"call_{data['u_phone']}"),
        InlineKeyboardButton("📢 Kanal", url="https://t.me/MADIWAYy"),
        InlineKeyboardButton("👥 Guruh", url="https://t.me/MADIWAY_Gr")
    )

    await bot.send_message(CHANNEL_ID, text, reply_markup=kb, parse_mode="Markdown")
    try:
        await bot.send_message(GROUP_ID, text, message_thread_id=data['t_id'])
    except:
        await bot.send_message(GROUP_ID, text)

# --- GURUH FILTRI ---
@dp.message_handler(chat_id=GROUP_ID)
async def filter_group(message: types.Message):
    if not message.text: return
    txt = message.text.lower()
    
    if message.from_user.username in ["yusufxonpro1", "madiways"]:
        return

    if any(word in txt for word in BAD_WORDS) or ("http" in txt or "@" in txt):
        await message.delete()
        if any(word in txt for word in BAD_WORDS):
            ban_time = datetime.datetime.now() + datetime.timedelta(days=2)
            await bot.restrict_chat_member(GROUP_ID, message.from_user.id, until_date=ban_time)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
