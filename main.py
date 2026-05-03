import logging
import json
import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# --- ASOSIY SOZLAMALAR ---
TOKEN = "8791239714:AAGeDUktKzciq9ftUp4lZZOzIuyItQXv5wM"
GROUP_ID = -1003996104316
CHANNEL_ID = "@MADIWAYy"
BANNER_URL = "https://raw.githubusercontent.com/madiway/madiway-bot/main/madiway_banner.png"
WEB_APP_URL = "https://madiway.github.io/madiway-bot/"

# --- SO'KINISHLAR VA TAQIQLANGAN SO'ZLAR RO'YXATI ---
BAD_WORDS = [
    "sokish1", "sokish2", "jalab", "skachat", "qo'toq", "am", "qotoq", "shalpang", 
    "iflos", "yaramas", "itdan tarqagan", "dalbayob", "axmoq", "onangni", "otangni", 
    "gey", "pider", "gandon", "lox", "tovuqmiya", "manqurt", "qaltis", "beshaka"
]

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# --- START BUYRUG'I (BANNER VA TUGMA BILAN) ---
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    start_kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="🚛 Ilovaga kirish", web_app=WebAppInfo(url=WEB_APP_URL))
    )
    
    caption = (
        "🏔 **MadiWay | Global Logistics & Dispatch 🚀**\n\n"
        "Xalqaro yuk tashish va professional dispetcherlik xizmatlari tarmog'iga xush kelibsiz!\n"
        "Biz to'rtta davlatni yagona xavfsiz marshrut bilan bog'laymiz:\n\n"
        "🌍 **Bizning yo'nalishlar:**\n"
        "📍 O'zbekiston 🇺🇿, Qozog'iston 🇰🇿, Rossiya 🇷🇺, Ozarbayjon 🇦🇿\n\n"
        "🚛 **MadiWay — Sizning yukingiz, bizning mas'uliyatimiz!**\n"
        "📥 @Madiways | 👥 @MADIWAY_Gr"
    )
    
    try:
        await bot.send_photo(message.chat.id, photo=BANNER_URL, caption=caption, reply_markup=start_kb, parse_mode="Markdown")
    except:
        await message.answer(caption, reply_markup=start_kb, parse_mode="Markdown")

# --- YUK YUBORISH (WEB APP DAN KELGAN DATA) ---
@dp.message_handler(content_types=['web_app_data'])
async def handle_webapp_data(message: types.Message):
    data = json.loads(message.web_app_data.data)
    now = datetime.datetime.now().strftime("%d.%m.%Y | %H:%M")
    
    report = (
        f"🚛 **YANGI YUK E'LONI**\n\n"
        f"📍 Yo'nalish: #{data['t_name']}\n"
        f"📦 Tavsif: {data['desc']}\n"
        f"⏰ Vaqt: {data['time']}\n"
        f"👤 Yuboruvchi: {data['u_name']}\n"
        f"📅 Sana: {now}"
    )

    kb = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("🤖 Bot", url="https://t.me/MADIWAYy_bot"),
        InlineKeyboardButton("📩 Lichka", url=f"tg://user?id={message.from_user.id}"),
        InlineKeyboardButton("📞 Raqam", callback_data=f"tel_{data['u_phone']}"),
        InlineKeyboardButton("📢 Kanal", url="https://t.me/MADIWAYy"),
        InlineKeyboardButton("👥 Guruh", url="https://t.me/MADIWAY_Gr")
    )

    await bot.send_message(CHANNEL_ID, report, reply_markup=kb, parse_mode="Markdown")
    try:
        await bot.send_message(GROUP_ID, report, message_thread_id=data['t_id'])
    except:
        await bot.send_message(GROUP_ID, report)

# --- GURUH FILTRI (SO'KINISH VA REKLAMA) ---
@dp.message_handler(chat_id=GROUP_ID)
async def group_filter(message: types.Message):
    if not message.text: return
    text = message.text.lower()
    
    # Adminlarni tekshirmaymiz
    if message.from_user.username in ["yusufxonpro1", "madiways"]:
        return

    # Reklama yoki so'kinishni aniqlash
    has_bad_word = any(word in text for word in BAD_WORDS)
    has_link = "http" in text or "@" in text

    if has_bad_word or has_link:
        await message.delete()
        if has_bad_word:
            # 2 kunga ban
            until = datetime.datetime.now() + datetime.timedelta(days=2)
            await bot.restrict_chat_member(GROUP_ID, message.from_user.id, until_date=until)
            await message.answer(f"🚫 {message.from_user.full_name} 2 kunga ban qilindi (Sabab: So'kinish).")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
