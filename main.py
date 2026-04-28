import logging
import json
import base64
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from aiohttp import web

# Railway Variables (Settings -> Variables bo'limidan olinadi)
API_TOKEN = os.getenv('API_TOKEN')
KANAL_ID = os.getenv('KANAL_ID', '@MADIWAYy')
ADMIN_ID = int(os.getenv('ADMIN_ID', 7402636402))
WEB_APP_URL = os.getenv('WEB_APP_URL', 'https://madiway.github.io/madiway-bot/')

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Railway o'chib qolmasligi uchun Health Check
async def handle(request):
    return web.Response(text="MadiWay Bot Online")

app = web.Application()
app.router.add_get('/', handle)

async def on_startup(dp):
    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

# --- START BUYRUG'I (SIZNING DESCRIPTION BILAN) ---
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    description_text = (
        "🏔 **MadiWay | Global Logistics & Dispatch** 🚀\n\n"
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
    
    # WebApp tugmasi
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🏔 MadiWay Ilovasi", web_app=WebAppInfo(url=WEB_APP_URL)))
    
    # Faqat Admin uchun tugma
    if message.from_user.id == ADMIN_ID:
        kb.add(KeyboardButton("⚙️ Admin Panel", web_app=WebAppInfo(url=f"{WEB_APP_URL}?admin=true")))
    
    await message.answer(description_text, parse_mode="Markdown", reply_markup=kb)

# --- WEB APP MA'LUMOTLARINI QAYTA ISHLASH ---
@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def web_app_data_handler(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        user = message.from_user

        # Yukni kanalga yuborish (0.1 soniya tezlik bilan)
        if data.get("action") == "post":
            repeat = int(data.get("repeat", 1))
            
            channel_kb = InlineKeyboardMarkup(row_width=2)
            channel_kb.add(
                InlineKeyboardButton("🚚 Yukni olish", url=f"tg://user?id={user.id}"),
                InlineKeyboardButton("👤 Yuk egasi", url=f"https://t.me/{user.username}" if user.username else f"tg://user?id={user.id}")
            )

            msg_text = (f"🏔 **MadiWay | YANGI YUK**\n"
                        f"───────────────────\n"
                        f"{data.get('content')}\n"
                        f"───────────────────\n"
                        f"📍 Kanal: {KANAL_ID}\n\n"
                        f"🔗 Kanalimiz: https://t.me/{KANAL_ID.replace('@', '')}")
            
            for _ in range(repeat):
                await bot.send_message(KANAL_ID, msg_text, reply_markup=channel_kb, parse_mode="Markdown")
                await asyncio.sleep(0.1)

            await message.answer(f"✅ Yukingiz {repeat} marta kanalga yuborildi!")

    except Exception as e:
        logging.error(f"Xatolik: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
