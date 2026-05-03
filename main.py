import logging
import json
import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# --- KONFIGURATSIYA ---
TOKEN = "8791239714:AAGeDUktKzciq9ftUp4lZZOzIuyItQXv5wM"
GROUP_ID = -1003996104316
CHANNEL_ID = "@MADIWAYy"
# Rasm manzili (GitHub'dagi manzilingiz)
BANNER_URL = "https://raw.githubusercontent.com/madiway/madiway-bot/main/madiway_banner.png"
WEB_APP_URL = "https://madiway.github.io/madiway-bot/"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# --- SO'KINISHLAR RO'YXATI ---
BAD_WORDS = [
    "sokish1", "sokish2", "jalab", "skachat", "qo'toq", "am", "qotoq", "shalpang", 
    "iflos", "yaramas", "itdan tarqagan", "dalbayob", "axmoq", "onangni", "otangni", 
    "gey", "pider", "gandon", "lox", "tovuqmiya", "manqurt", "qaltis", "beshaka"
]

# --- START BUYRUG'I (BANNER VA TUGMA BILAN) ---
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="🚛 Ilovaga kirish", web_app=WebAppInfo(url=WEB_APP_URL))
    )
    
    caption = (
        "🏔 **MadiWay | Global Logistics & Dispatch 🚀**\n\n"
        "Xalqaro yuk tashish va professional dispetcherlik xizmatlari tarmog'iga xush kelibsiz! "
        "Biz to'rtta davlatni yagona xavfsiz marshrut bilan bog'laymiz:\n\n"
        "🌍 **Bizning yo'nalishlar:**\n"
        "📍 O'zbekiston 🇺🇿, Qozog'iston 🇰🇿, Rossiya 🇷🇺, Ozarbayjon 🇦🇿\n\n"
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
        await bot.send_photo(message.chat.id, photo=BANNER_URL, caption=caption, reply_markup=kb, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Start xatosi: {e}")
        await message.answer(caption, reply_markup=kb, parse_mode="Markdown")

# --- YUK YUBORISH (WEB APP DATA) ---
@dp.message_handler(content_types=['web_app_data'])
async def web_app_data_handler(message: types.Message):
    try:
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

        kb = InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton("🤖 Bot", url="https://t.me/MADIWAYy_bot"),
            InlineKeyboardButton("📩 Lichka", url=f"tg://user?id={message.from_user.id}"),
            InlineKeyboardButton("📞 Raqam", callback_data=f"call_{data['u_phone']}"),
            InlineKeyboardButton("📢 Kanal", url="https://t.me/MADIWAYy"),
            InlineKeyboardButton("👥 Guruh", url="https://t.me/MADIWAY_Gr")
        )

        await bot.send_message(CHANNEL_ID, text, reply_markup=kb, parse_mode="Markdown")
        try:
            # Guruhga yo'nalish bo'yicha yuborish
            await bot.send_message(GROUP_ID, text, message_thread_id=data['t_id'])
        except:
            await bot.send_message(GROUP_ID, text)
            
    except Exception as e:
        logging.error(f"Data error: {e}")

# --- GURUH FILTRI (SO'KINISH VA REKLAMA) ---
@dp.message_handler(chat_id=GROUP_ID)
async def group_filter(message: types.Message):
    if not message.text: return
    txt = message.text.lower()
    
    # Adminlarni tekshirmaymiz
    if message.from_user.username in ["yusufxonpro1", "madiways"]:
        return

    # So'kinish yoki reklama bo'lsa
    if any(word in txt for word in BAD_WORDS) or ("http" in txt or "@" in txt):
        await message.delete()
        if any(word in txt for word in BAD_WORDS):
            # 2 kunga ban (48 soat)
            ban_until = datetime.datetime.now() + datetime.timedelta(days=2)
            await bot.restrict_chat_member(GROUP_ID, message.from_user.id, until_date=ban_until)
            await message.answer(f"🚫 {message.from_user.full_name} 2 kunga jazolandi (Sabab: So'kinish).")

if __name__ == "__main__":
    # skip_updates=True bot o'chiq turganda yig'ilib qolgan eski xabarlarni o'chiradi
    executor.start_polling(dp, skip_updates=True)
