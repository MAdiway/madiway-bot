import logging
import json
import base64
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from aiohttp import web

# Railway Variables
API_TOKEN = os.getenv('API_TOKEN')
KANAL_ID = os.getenv('KANAL_ID', '@MADIWAYy')
ADMIN_ID = int(os.getenv('ADMIN_ID', 7402636402))
WEB_APP_URL = os.getenv('WEB_APP_URL', 'https://madiway.github.io/madiway-bot/')

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Railway serveri o'chib qolmasligi uchun (Health Check)
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

# --- START BUYRUG'I ---
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    start_text = (
        "🏔 **MadiWay | Global Logistics & Dispatch** 🚀\n\n"
        "Xalqaro yuk tashish tizimiga xush kelibsiz!\n\n"
        "🌍 **Bizning yo'nalishlar:**\n"
        "📍 O'zbekiston, Qozog'iston, Rossiya, Ozarbayjon.\n\n"
        "🚛 **MadiWay — Sizning yukingiz, bizning mas'uliyatimiz!**\n"
        "📞 Tel: +998 (91) 944-70-08"
    )
    
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🏔 MadiWay Ilovasi", web_app=WebAppInfo(url=WEB_APP_URL)))
    
    if message.from_user.id == ADMIN_ID:
        kb.add(KeyboardButton("⚙️ Admin Panel", web_app=WebAppInfo(url=f"{WEB_APP_URL}?admin=true")))
    
    await message.answer(start_text, parse_mode="Markdown", reply_markup=kb)

# --- MA'LUMOTLARNI QABUL QILISH (WEB APP DATA) ---
@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def web_app_data_handler(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        user = message.from_user

        # Face ID rasmi kelsa
        if "auth" in data:
            img_bytes = base64.b64decode(data["auth"]["img"].split(',')[1])
            with open("verify.jpg", "wb") as f: f.write(img_bytes)
            cap = f"👤 **Face ID:** {data['auth']['name']}\n📞 **Tel:** {data['auth']['phone']}"
            await bot.send_photo(ADMIN_ID, types.InputFile("verify.jpg"), caption=cap)
            os.remove("verify.jpg")

        # Yukni kanalga 0.1s da yuborish
        if data.get("action") == "post":
            repeat = int(data.get("repeat", 1))
            channel_kb = InlineKeyboardMarkup().add(
                InlineKeyboardButton("🚚 Yukni olish", url=f"tg://user?id={user.id}"),
                InlineKeyboardButton("👤 Yuk egasi", url=f"https://t.me/{user.username}" if user.username else f"tg://user?id={user.id}")
            )
            msg = (f"🏔 **MADIWAY YUK**\n"
                   f"───────────────────\n"
                   f"{data['content']}\n"
                   f"───────────────────\n"
                   f"🔗 Kanal: https://t.me/{KANAL_ID.replace('@','')}")
            
            for _ in range(repeat):
                await bot.send_message(KANAL_ID, msg, reply_markup=channel_kb)
                await asyncio.sleep(0.1)
                
            await message.answer("✅ Yuk kanalga yuborildi!")
    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
