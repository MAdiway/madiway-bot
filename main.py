import logging
import json
import base64
import asyncio
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
BANNER_IMG = "madiway banner.jpg"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Ma'lumotlarni saqlash
user_limits = {} 
chat_history = {}

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    is_admin = user_id in ADMINS
    
    # Status belgisini aniqlash
    status_icon = "🛡 **Siz tizimda: Admin ✅**" if is_admin else "👤 **Siz tizimda: Foydalanuvchi**"
    
    # Siz yuborgan aniq matn
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
    
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    kb.add(KeyboardButton("🏔 MadiWay Ilovasi", web_app=WebAppInfo(url=WEB_APP_URL)))
    
    if is_admin:
        kb.add(KeyboardButton("📩 Chat Monitoring (Lichkalar)"))

    try:
        with open(BANNER_IMG, 'rb') as photo:
            await message.answer_photo(photo, caption=msg_text, parse_mode="Markdown", reply_markup=kb)
    except Exception:
        await message.answer(msg_text, parse_mode="Markdown", reply_markup=kb)

# --- CHAT MONITORING (Lichkani kuzatish) ---
@dp.message_handler(lambda m: m.chat.type == 'private' and not m.text.startswith('/'))
async def monitor_private_chats(message: types.Message):
    if message.from_user.id in ADMINS: return
    
    uid = message.from_user.id
    log_msg = f"🕒 {datetime.now().strftime('%H:%M:%S')} | {message.text}"
    
    if uid not in chat_history: chat_history[uid] = []
    chat_history[uid].append(log_msg)

    # Adminlarga srazu bildirish
    for admin in ADMINS:
        try:
            await bot.send_message(admin, f"👁 **Lichka Monitoring:**\n👤 {message.from_user.full_name}\n🆔 `{uid}`\n💬 {message.text}", parse_mode="Markdown")
        except: pass

# --- WEB APP DATA (Yuk va Face ID) ---
@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def web_app_data_handler(message: types.Message):
    data = json.loads(message.web_app_data.data)
    user = message.from_user
    now = datetime.now()

    # Face ID hisoboti (Login bo'lganda)
    if data.get("action") == "login_report":
        auth = data.get("auth")
        img_bytes = base64.b64decode(auth['img'].split(',')[1])
        caption = f"👤 **FACE ID LOGIN**\n\n👤 {auth['name']}\n📞 {auth['phone']}\n🆔 `{user.id}`"
        for admin in ADMINS:
            try: await bot.send_photo(admin, BytesIO(img_bytes), caption=caption, parse_mode="Markdown")
            except: pass
        return

    # Yukni kanalga chiqarish
    if data.get("action") == "post":
        # 55 kunlik cheklov
        if user.id not in ADMINS:
            if user.id in user_limits:
                if now < user_limits[user.id] + timedelta(days=55):
                    wait = (user_limits[user.id] + timedelta(days=55)) - now
                    return await message.answer(f"⚠️ Cheklov: Yana {wait.days} kundan keyin yuk qo'sha olasiz!")
            user_limits[user.id] = now

        # Kanal uchun post matni
        post_text = (
            f"🚛 **#YANGI_YUK**\n\n"
            f"📦 **Tavsif:** {data['content']}\n"
            f"⏰ **Vaqt:** {data['time']}\n"
            f"🔄 **Takrorlanish:** {data['repeat']} marta\n\n"
            f"👤 **Yuboruvchi:** {user.first_name}\n"
            f"🕒 **Sana:** {now.strftime('%d/%m/%Y | %H:%M')}\n\n"
            f"🏁 @MADIWAYy"
        )

        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(
            InlineKeyboardButton("📞 Raqamni ko'rish", callback_data=f"tel_{user.id}"),
            InlineKeyboardButton("💬 Lichkaga yozish", url=f"tg://user?id={user.id}"),
            InlineKeyboardButton("🚀 Yuk Joylash", url=f"https://t.me/madiway_bot?start=post")
        )

        await bot.send_message(KANAL_ID, post_text, reply_markup=kb, parse_mode="Markdown")
        await message.answer("✅ Yukingiz kanalga chiqdi va monitoringga olindi!")

# --- ADMIN MONITORING TIZIMI ---
@dp.message_handler(lambda m: m.text == "📩 Chat Monitoring (Lichkalar)")
async def show_monitor(message: types.Message):
    if message.from_user.id not in ADMINS: return
    if not chat_history: return await message.answer("Hozircha chatlar tarixi bo'sh.")
    
    report = "📋 **Chatlar Monitoringi:**\n\n"
    for uid, msgs in chat_history.items():
        report += f"👤 User ID: `{uid}`\n" + "\n".join(msgs[-3:]) + "\n---\n"
    
    await message.answer(report[:4000], parse_mode="Markdown")

@dp.callback_query_handler(lambda c: c.data.startswith('tel_'))
async def show_tel(callback: types.CallbackQuery):
    await callback.answer("📞 Aloqa uchun 'Lichkaga yozish' tugmasidan foydalaning!", show_alert=True)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
