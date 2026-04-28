import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

# Sozlamalar
API_TOKEN = os.getenv('API_TOKEN')
WEB_APP_URL = os.getenv('WEB_APP_URL')
PORT = int(os.getenv('PORT', 8080))

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    desc = (
        ""🏔 **MadiWay | Global Logistics & Dispatch** 🚀\n\n"
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
        "📞 Tel: +998 (91) 944-70-08"
    )
    kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("🏔 MadiWay Ilovasi", web_app=WebAppInfo(url=WEB_APP_URL))
    )
    await message.answer(desc, parse_mode="Markdown", reply_markup=kb)

# Railway o'chib qolmasligi uchun oddiy server
async def on_startup(x):
    logging.info(f"Bot 3.10 versiyada ishga tushdi. Port: {PORT}")

if __name__ == '__main__':
    # Railway'da polling usulida ishlatamiz
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
