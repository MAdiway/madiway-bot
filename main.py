import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- SOZLAMALAR ---
BOT_TOKEN = "8724439262:AAFGNuQQ4IxdqitlcCEtkHLsvyFwSPg_b1c"
BOT_USERNAME = "MADIWAYy_Bot"

# Botni ishga tushirish
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# --- KLAVIATURA ---
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("📞 Nomerni ko'rish", url=f"https://t.me/{BOT_USERNAME}?start=get_number"),
        InlineKeyboardButton("📱 Programma", url=f"https://t.me/{BOT_USERNAME}?start=app"),
        InlineKeyboardButton("📢 Kanalimiz", url="https://t.me/MADIWAYy")
    )
    return keyboard

# --- START BUYRUG'I ---
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    welcome_text = (
        "🏔 <b>MadiWay | Global Logistics & Dispatch</b> 🚀\n\n"
        "Xalqaro yuk tashish va professional dispetcherlik xizmatlari tarmog'iga xush kelibsiz!\n\n"
        "🌍 <b>Bizning yo'nalishlar:</b>\n"
        "📍 O'zbekiston 🇺🇿, Qozog'iston 🇰🇿, Rossiya 🇷🇺, Ozarbayjon 🇦🇿\n\n"
        "🛡 <b>Nega MadiWay?</b>\n"
        "✅ Ishonchlilik, Tezkorlik, 24/7 Professional Dispetcherlik.\n\n"
        "🚛 <b>MadiWay — Sizning yukingiz, bizning mas'uliyatimiz!</b>\n\n"
        "📥 Bog'lanish uchun: @Madiways\n"
        "🔗 Link: T.me/MADIWAYy\n"
        "👥 Gruppa: Pullik lic @madiways"
    )
    try:
        # madiway_banner.png GitHub-da bo'lishi kerak
        with open("madiway_banner.png", "rb") as photo:
            await bot.send_photo(message.chat.id, photo, caption=welcome_text, reply_markup=get_main_keyboard())
    except:
        # Rasm topilmasa faqat matn yuboriladi
        await message.answer(welcome_text, reply_markup=get_main_keyboard())

# --- ASOSIY ISHGA TUSHIRISH ---
if __name__ == "__main__":
    print("✅ MadiWay Bot faqat Bot rejimida ishga tushdi!")
    executor.start_polling(dp, skip_updates=True)
