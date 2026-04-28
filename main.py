import os
import json
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

# SOZLAMALAR
TOKEN = "8791239714:AAH17eobRUq3xCUMYJipwcSrmYPJPfZr3Rs"
KANAL_ID = "@MADIWAYy"
ADMINS = [7402636402, 5123456789] # Yusufxonpro1 va Madiways ID'larini bosing
WEB_APP_URL = "https://madiway.github.io/madiway-bot/" # GitHub linkinigiz

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# RAILWAY HEALTH CHECK (O'CHIB QOLMASLIK UCHUN)
async def handle(request):
    return web.Response(text="MadiWay Bot is Running 24/7")

app = web.Application()
app.router.add_get('/', handle)

async def on_startup(dp):
    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', port).start()

# --- BOT BUYRUQLARI ---
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    desc = (
        "🏔 **MadiWay | Global Logistics & Dispatch** 🚀\n\n"
        "Xalqaro yuk tashish va professional dispetcherlik xizmatlari tarmog'iga xush kelibsiz! "
        "Biz to'rtta davlatni yagona xavfsiz marshrut bilan bog'laymiz:\n\n"
        "🌍 **Bizning yo'nalishlar:**\n"
        "📍 O'zbekiston 🇺🇿, Qozog'iston 🇰🇿, Rossiya 🇷🇺, Ozarbayjon 🇦🇿\n\n"
        "🛡 **Nega aynan MadiWay?**\n"
        "✅ Ishonchlilik, Tezkorlik va 24/7 Aloqa.\n\n"
        "🚛 **MadiWay — Sizning yukingiz, bizning mas'uliyatimiz!**\n\n"
        "📥 Bog'lanish: [@Madiways]"
    )
    
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🏔 MadiWay Ilovasi", web_app=WebAppInfo(url=WEB_APP_URL)))
    
    # Faqat Adminlar uchun tugma
    if message.from_user.id in ADMINS:
        kb.add(KeyboardButton("⚙️ Admin Boshqaruvi", web_app=WebAppInfo(url=f"{WEB_APP_URL}?admin=true")))
        
    await message.answer(desc, parse_mode="Markdown", reply_markup=kb)

# --- WEB APP'DAN MA'LUMOT KELGANDA ---
@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def web_app_receive(message: types.Message):
    data = json.loads(message.web_app_data.data)
    user = message.from_user

    if data.get("action") == "post":
        # Kanalga yuboriladigan matn
        post_text = (
            f"🏔 **MadiWay | YANGI YUK**\n"
            f"───────────────────\n"
            f"📦 **Yuk:** {data['content']}\n"
            f"⏰ **Vaqt:** {data['time']}\n"
            f"───────────────────\n"
            f"📢 T.me/MADIWAYy"
        )

        # Inline tugmalar (Yukni ko'rish)
        btn_user = f"tg://user?id={user.id}"
        kb_inline = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🚚 Yukni ko'rish (To'liq)", callback_data=f"info_{user.id}_{data['time']}")
        )
        kb_inline.add(InlineKeyboardButton("🔗 MadiWay Kanal", url="https://t.me/MADIWAYy"))

        # Kanalga yuborish
        for _ in range(int(data.get('repeat', 1))):
            await bot.send_message(KANAL_ID, post_text, reply_markup=kb_inline, parse_mode="Markdown")
            await asyncio.sleep(0.1)
        
        await message.answer("✅ Yukingiz kanalga yuborildi!")

# Yuk egasining ma'lumotlarini ko'rsatish
@dp.callback_query_handler(lambda c: c.data.startswith('info_'))
async def callback_info(callback: types.CallbackQuery):
    user_id = callback.data.split('_')[1]
    # Bu yerda foydalanuvchi ma'lumotlarini yuboramiz
    await callback.answer(f"Yuk egasi bilan bog'lanish:\ntg://user?id={user_id}", show_alert=True)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
