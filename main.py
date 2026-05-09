import asyncio
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# --- SOZLAMALAR ---
BOT_TOKEN = "8724439262:AAFGNuQQ4IxdqitlcCEtkHLsvyFwSPg_b1c"
BOT_USERNAME = "MADIWAYy_Bot"
# Railway'dagi manzilingni bu yerga yoz (masalan: https://madiway.up.railway.app)
WEB_APP_URL = "https://SENING_RAILWAY_URLING.up.railway.app/index.html"

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# --- KLAVIATURA ---
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("🚚 Yuk yuborish (Web App)", web_app=WebAppInfo(url=WEB_APP_URL)),
        InlineKeyboardButton("📢 Kanalimiz", url="https://t.me/MADIWAYy"),
        InlineKeyboardButton("👥 Guruhimiz", url="https://t.me/+826yU-9lW6I1YmQy")
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
        "🚛 <b>MadiWay — Sizning yukingiz, bizning mas'uliyatimiz!</b>\n\n"
        "Pastdagi tugma orqali yuk ma'lumotlarini yuborishingiz mumkin 👇"
    )
    try:
        with open("madiway_banner.png", "rb") as photo:
            await bot.send_photo(message.chat.id, photo, caption=welcome_text, reply_markup=get_main_keyboard())
    except:
        await message.answer(welcome_text, reply_markup=get_main_keyboard())

if __name__ == "__main__":
    print("✅ MadiWay Bot ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)
