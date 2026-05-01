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
BANNER_URL = "https://madiway.github.io/madiway-bot/madiway_banner.png"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

user_limits = {} 

# 1. START BUYRUG'I
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
        await message.answer_photo(photo=BANNER_URL, caption=msg_text, parse_mode="Markdown", reply_markup=kb)
    except:
        await message.answer(msg_text, parse_mode="Markdown", reply_markup=kb)

# 2. KANALGA YUK YUBORISH (4 TA TUGMA BILAN)
@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def web_app_data_handler(message: types.Message):
    data = json.loads(message.web_app_data.data)
    user = message.from_user
    now = datetime.now()

    if data.get("action") == "post":
        # 55 kunlik cheklov (Admin bo'lmasa)
        if user.id not in ADMINS:
            if user.id in user_limits:
                if now < user_limits[user.id] + timedelta(days=55):
                    return await message.answer(f"⚠️ Limit: { (user_limits[user.id] + timedelta(days=55) - now).days } kundan keyin yuk qo'sha olasiz.")
            user_limits[user.id] = now

        post_text = (
            f"🚛 **#YANGI_YUK | MadiWay**\n\n"
            f"📦 **Tavsif:** {data['content']}\n"
            f"⏰ **Yuklash vaqti:** {data['time']}\n"
            f"🔄 **Soni:** {data['repeat']} marta\n"
            f"👤 **E'lon beruvchi:** {user.full_name}\n"
            f"📅 **Sana:** {now.strftime('%d/%m/%Y')}\n\n"
            f"🏁 @MADIWAYy"
        )
        
        # SIZ AYTGAN 4 TA TUGMA
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton("📞 Raqamni ko'rish", callback_data=f"tel_{user.id}"),
            InlineKeyboardButton("🚀 Yuk Joylash", url="https://t.me/madiway_bot?start=post"),
            InlineKeyboardButton("🏔 MadiWay Kanal", url="https://t.me/MADIWAYy"),
            InlineKeyboardButton("💬 Lichkaga yozish", url=f"tg://user?id={user.id}")
        )
        
        await bot.send_message(KANAL_ID, post_text, reply_markup=kb, parse_mode="Markdown")
        await message.answer("✅ Yukingiz kanalga barcha tugmalar bilan muvaffaqiyatli yuborildi!")

# 3. LICHKA MONITORING (Chatni kuzatish)
@dp.message_handler(lambda m: m.chat.type == 'private' and not m.text.startswith('/'))
async def track_chat(message: types.Message):
    if message.from_user.id in ADMINS: return
    for admin in ADMINS:
        try:
            await bot.send_message(admin, f"👁 **Chat Monitor:**\n👤 {message.from_user.full_name}\n🆔 `{message.from_user.id}`\n💬 {message.text}")
        except: pass

# Tugma bosilganda alert chiqarish (Raqam uchun)
@dp.callback_query_handler(lambda c: c.data.startswith('tel_'))
async def tel_callback(callback: types.CallbackQuery):
    await callback.answer("📞 Aloqa uchun 'Lichkaga yozish' tugmasi orqali profilga o'ting!", show_alert=True)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
