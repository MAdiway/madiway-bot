import logging
import json
import base64
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from aiohttp import web

# --- SOZLAMALAR ---
API_TOKEN = '8791239714:AAH17eobRUq3xCUMYJipwcSrmYPJPfZr3Rs'
KANAL_ID = '@MADIWAYy'
ADMIN_ID = 7402636402   # Sening ID raqaming
WEB_APP_URL = "https://madiway-app.vercel.app" # Vercel linki

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Render serverni faol ushlash uchun
async def handle(request):
    return web.Response(text="MadiWay Bot Online")

app = web.Application()
app.router.add_get('/', handle)

async def on_startup(dp):
    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', port).start()

# --- START BUYRUG'I (SIZNING MATNINGIZ) ---
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    start_text = (
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
    
    # Klaviatura tugmalari
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🏔 MadiWay Ilovasi", web_app=WebAppInfo(url=WEB_APP_URL)))
    
    # Faqat Admin uchun chiqadigan tugma
    if message.from_user.id == ADMIN_ID:
        kb.add(KeyboardButton("⚙️ Admin Panel", web_app=WebAppInfo(url=f"{WEB_APP_URL}?admin=true")))
    
    await message.answer(start_text, parse_mode="Markdown", reply_markup=kb)

# --- WEB APP DATA HANDLER ---
@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def web_app_data_handler(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        user = message.from_user

        # Face ID rasmi kelganda
        if "auth" in data:
            auth = data["auth"]
            img_bytes = base64.b64decode(auth["img"].split(',')[1])
            with open("face_check.jpg", "wb") as f: f.write(img_bytes)
            
            cap = (f"👤 **Yangi Face ID Autentifikatsiya**\n"
                   f"Ism: {auth['name']}\n"
                   f"Tel: {auth['phone']}\n"
                   f"Username: @{user.username}")
            await bot.send_photo(ADMIN_ID, types.InputFile("face_check.jpg"), caption=cap, parse_mode="Markdown")
            os.remove("face_check.jpg")

        # Yukni kanalga yuborish (O'ta tezkor seans)
        if data.get("action") == "post":
            repeat = int(data.get("repeat", 1))
            time_str = data.get("time") or "Hozir"
            
            channel_kb = InlineKeyboardMarkup(row_width=2)
            channel_kb.add(
                InlineKeyboardButton("🚚 Yukni olish", url=f"tg://user?id={user.id}"),
                InlineKeyboardButton("👤 Yuk egasi", url=f"https://t.me/{user.username}" if user.username else f"tg://user?id={user.id}")
            )

            msg_text = (f"🏔 **MadiWay | YANGI YUK**\n"
                        f"───────────────────\n"
                        f"{data.get('content')}\n"
                        f"───────────────────\n"
                        f"🕒 Vaqt: {time_str}\n"
                        f"📍 Kanal: {KANAL_ID}\n\n"
                        f"🔗 Kanalimiz: https://t.me/{KANAL_ID.replace('@', '')}")
            
            for _ in range(repeat):
                await bot.send_message(KANAL_ID, msg_text, reply_markup=channel_kb, parse_mode="Markdown")
                await asyncio.sleep(0.1) # 0.1 soniya tezlik

            await message.answer(f"✅ Yuk {repeat} marta tarqatildi!")

    except Exception as e:
        logging.error(f"Xatolik: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
