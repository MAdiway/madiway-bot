import logging
import json
import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# Sozlamalar
TOKEN = "8791239714:AAGeDUktKzciq9ftUp4lZZOzIuyItQXv5wM" 
GROUP_ID = -1003996104316 
CHANNEL_ID = "@MADIWAYy" 
BANNER_URL = "https://raw.githubusercontent.com/madiway/madiway-bot/main/madiway_banner.png"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# So'kinishlar ro'yxati (Buni kengaytirishingiz mumkin)
BAD_WORDS = ["sokish1", "yomon_soz", "admin_emas , "jalab , oneniami" , "yiban , "ko't , "skaman , "pidaraz , "ko'tingdi qis , skachat", "qo'toq", "am", "qotoq", "shalpang", 
    "iflos", "yaramas", "itdan tarqagan", "dalbayob", "axmoq", "onangni", "otangni", 
    "gey", "pider", "gandon", "lox", "tovuqmiya", "manqurt", "qaltis", "beshaka"
"]

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(text="🚛 Yuk yuborish", web_app=WebAppInfo(url="Sizning_URL")))
    
    caption = (
        "🏔 **MadiWay | Global Logistics & Dispatch 🚀**\n\n"
        "Xalqaro yuk tashish va professional dispetcherlik xizmatlari tarmog'iga xush kelibsiz!\n"
        "📍 O'zbekiston 🇺🇿, Qozog'iston 🇰🇿, Rossiya 🇷🇺, Ozarbayjon 🇦🇿\n\n"
        "🚛 **MadiWay — Sizning yukingiz, bizning mas'uliyatimiz!**"
    )
    await bot.send_photo(chat_id=message.chat.id, photo=BANNER_URL, caption=caption, reply_markup=kb, parse_mode="Markdown")

@dp.message_handler(content_types=['web_app_data'])
async def handle_webapp_data(message: types.Message):
    res = json.loads(message.web_app_data.data)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    report = (
        f"🚛 **YANGI YUK E'LONI**\n\n"
        f"📍 Yo'nalish: #{res['t_name']}\n"
        f"📦 Tavsif: {res['desc']}\n"
        f"⏰ Vaqt: {res['time']}\n"
        f"👤 Yuboruvchi: {res['u_name']}\n"
        f"📅 Sana: {now}\n"
    )

    # Kanal uchun 5 ta maxsus tugma
    channel_kb = InlineKeyboardMarkup(row_width=2)
    channel_kb.add(
        InlineKeyboardButton("🤖 Bot", url="https://t.me/MADIWAYy_bot"),
        InlineKeyboardButton("📩 Yukni egasi (Lichka)", url=f"tg://user?id={message.from_user.id}"),
        InlineKeyboardButton("📞 Yukchi raqami", callback_data=f"show_tel_{res['u_phone']}"),
        InlineKeyboardButton("📢 Kanal", url="https://t.me/MADIWAYy"),
        InlineKeyboardButton("👥 Guruh", url="https://t.me/MADIWAY_Gr")
    )

    await bot.send_message(chat_id=CHANNEL_ID, text=report, reply_markup=channel_kb, parse_mode="Markdown")
    try:
        await bot.send_message(chat_id=GROUP_ID, message_thread_id=res['t_id'], text=report)
    except:
        await bot.send_message(chat_id=GROUP_ID, text=report)

# Guruh filtri (Reklama va So'kinish uchun)
@dp.message_handler(chat_id=GROUP_ID)
async def monitor_group(message: types.Message):
    if message.from_user.is_bot: return
    
    # Reklama tekshiruvi (faqat adminlarga mumkin)
    if ("http" in message.text or "@" in message.text) and not (message.from_user.username in ["madiways", "yusufxonpro1"]):
        await message.delete()
        return

    # So'kinish tekshiruvi
    if any(word in message.text.lower() for word in BAD_WORDS):
        await message.delete()
        # 2 kunga ban qilish
        until = datetime.datetime.now() + datetime.timedelta(days=2)
        await bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=until)
        await message.answer(f"🚫 {message.from_user.first_name} 2 kunga ban qilindi (Sabab: So'kinish)")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
