import logging
import json
import base64
from datetime import datetime, timedelta
from io import BytesIO
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# --- KONFIGURATSIYA ---
TOKEN = "8791239714:AAH17eobRUq3xCUMYJipwcSrmYPJPfZr3Rs"
ADMINS = [6977836294, 8112179116] 
KANAL_ID = "@MADIWAYy"
WEB_APP_URL = "https://madiway.github.io/madiway-bot/" 

# Rasm nomi (GitHub'da ham shundayligini tekshiring)
BANNER_IMG = "madiway_banner.png" 

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

user_limits = {} 
chat_history = {}

# 1. START - RASM VA SIZ BERGAN MATN BILAN
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    is_admin = user_id in ADMINS
    status_icon = "🛡 **Siz tizimda: Admin ✅**" if is_admin else "👤 **Siz tizimda: Foydalanuvchi**"
    
    msg_text = (
        "🏔 **MadiWay | Global Logistics & Dispatch** 🚀\n\n"
        "Xalqaro yuk tashish va professional dispetcherlik xizmatlari tarmog'iga xush kelibsiz!\n"
        "Biz to'rtta davlatni yagona xavfsiz marshrut bilan bog'laymiz:\n\n"
        "🌍 **Bizning yo'nalishlar:**\n"
        "📍 O'zbekiston 🇺🇿\n"
        "📍 Qozog'iston 🇰🇿\n"
        "📍 Rossiya 🇷🇺\n"
        "📍 Ozarbayjon 🇦🇿\n\n"
        f"{status_icon}\n\n"
        "✅ Ishonchlilik: Yukingiz manzili va vaqti bizning nazoratimizda.\n"
        "✅ Tezkorlik: Eng qulay va xavfsiz yo'llarni taqdim etamiz.\n"
        "✅ Professional Dispetcherlik: 24/7 aloqa va harakat nazorati.\n\n"
        "🚛 **MadiWay — Sizning yukingiz, bizning mas'uliyatimiz!**\n\n"
        "📥 Bog'lanish uchun: @Madiways\n"
        "🔗 Kanal: T.me/MADIWAYy"
    )
    
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🏔 MadiWay Ilovasi", web_app=WebAppInfo(url=WEB_APP_URL)))
    if is_admin:
        kb.add(KeyboardButton("📩 Chat Monitoring"))

    try:
        with open(BANNER_IMG, 'rb') as photo:
            await message.answer_photo(photo, caption=msg_text, parse_mode="Markdown", reply_markup=kb)
    except:
        await message.answer(msg_text, parse_mode="Markdown", reply_markup=kb)

# 2. WEB APP MA'LUMOTLARI VA KANALGA 4 TA TUGMA
@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def web_app_data_handler(message: types.Message):
    data = json.loads(message.web_app_data.data)
    user = message.from_user
    now = datetime.now()

    # Face ID Login Monitoring
    if data.get("action") == "login_report":
        auth = data.get("auth")
        img_bytes = base64.b64decode(auth['img'].split(',')[1])
        caption = f"👤 **FACE ID LOGIN**\n👤 {auth['name']}\n📞 {auth['phone']}\n🆔 `{user.id}`"
        for admin in ADMINS:
            try: await bot.send_photo(admin, BytesIO(img_bytes), caption=caption, parse_mode="Markdown")
            except: pass

    # Yuk e'loni
    elif data.get("action") == "post":
        if user.id not in ADMINS:
            if user.id in user_limits:
                if now < user_limits[user.id] + timedelta(days=55):
                    return await message.answer("⚠️ Limit: 55 kundan keyin yuk qo'sha olasiz.")
            user_limits[user.id] = now

        post_text = (
            f"🚛 **#YANGI_YUK | MadiWay**\n\n"
            f"📦 **Yuk:** {data['content']}\n"
            f"⏰ **Vaqt:** {data['time']}\n"
            f"🔄 **Soni:** {data['repeat']} marta\n"
            f"👤 **E'lon beruvchi:** {user.first_name}\n\n"
            f"🏁 @MADIWAYy"
        )
        
        # SIZ XOHLAGAN 4 TA TUGMA
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton("📞 Raqamni ko'rish", callback_data=f"tel_{user.id}"),
            InlineKeyboardButton("💬 Lichkaga yozish", url=f"tg://user?id={user.id}"),
            InlineKeyboardButton("🚀 Yuk Joylash", url=f"https://t.me/madiway_bot?start=post"),
            InlineKeyboardButton("🏔 Ilovaga kirish", url=WEB_APP_URL)
        )
        
        await bot.send_message(KANAL_ID, post_text, reply_markup=kb, parse_mode="Markdown")
        await message.answer("✅ Yukingiz kanalga 4 ta tugma bilan yuborildi!")

# 3. LICHKA MONITORING (Chatni kuzatish)
@dp.message_handler(lambda m: m.chat.type == 'private' and not m.text.startswith('/'))
async def track_chat(message: types.Message):
    if message.from_user.id in ADMINS: return
    for admin in ADMINS:
        try:
            await bot.send_message(admin, f"👁 **Chat Monitor:**\n👤 {message.from_user.full_name}\n💬 {message.text}")
        except: pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
