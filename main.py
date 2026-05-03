import logging
import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# Bot sozlamalari
TOKEN = "8791239714:AAH17eobRUq3xCUMYJipwcSrmYPJPfZr3Rs"
ADMINS = [6977836294, 8112179116]
KANAL_ID = "@MADIWAYy"
GROUP_ID = -1002345678901  # MADIWAY_Gr guruhining haqiqiy ID sini qo'ying

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Face ID rasmlari uchun vaqtinchalik baza
face_database = {}

# SIZ BERGAN TOPICLAR VA ULARNING ID-LARI
TOPICS = {
    "Europe": 2,
    "Rossiya": 4,
    "Qirg'iziston": 6,
    "Kazakistan": 8,
    "Eron": 10,
    "Tojikston": 12,
    "Germaniya": 14,
    "Belarusiya": 16,
    "Gruziya": 18,
    "Ukraina": 20
}

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🏔 MadiWay Ilovasi", web_app=WebAppInfo(url="https://madiway.github.io/madiway-bot/")),
    )
    
    # Faqat adminlar uchun Face ID bazasi tugmasi
    if message.from_user.id in ADMINS:
        kb.add(InlineKeyboardButton("📸 Face ID Skanerlar Bazasi", callback_data="view_face_db"))

    caption = (
        "🚛 **MADIWAY | Professional Logistics**\n\n"
        "Xalqaro yuk tashish tizimi va yuklarni boshqarish botiga xush kelibsiz!\n\n"
        "Pastdagi tugma orqali ilovaga kiring va yukingizni joylang."
    )
    
    await message.answer_photo(
        photo="https://i.postimg.cc/WbcqK7FF/daf-xf-daf-trucks-car-renault-magnum-car-removebg-preview.png",
        caption=caption,
        reply_markup=kb,
        parse_mode="Markdown"
    )

@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def handle_webapp_data(message: types.Message):
    data = json.loads(message.web_app_data.data)
    user = message.from_user

    # Face ID hisoboti (Login qilinganda)
    if data.get("action") == "login_report":
        face_database[user.id] = {
            "name": data['auth']['name'],
            "phone": data['auth']['phone'],
            "photo": data['auth']['img']
        }
        for admin in ADMINS:
            await bot.send_message(admin, f"👤 **Yangi Face ID Tasdiqlandi:**\nIsm: {data['auth']['name']}\nTel: {data['auth']['phone']}")

    # Yuk yuborish (Post)
    elif data.get("action") == "post":
        country = data.get("country")
        topic_id = TOPICS.get(country)
        count = int(data.get("repeat", 1)) 
        
        post_text = (
            f"🚛 **#YANGI_YUK | {country}**\n\n"
            f"📦 **Yuk:** {data['content']}\n"
            f"⏰ **Vaqt:** {data['time']}\n"
            f"👤 **E'lon beruvchi:** {user.full_name}\n"
            f"📞 **Aloqa:** Ilova orqali\n\n"
            f"🏁 @MADIWAYy | @MADIWAYy_bot"
        )
        
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton("📞 Raqamni ko'rish", callback_data=f"show_tel_{user.id}"),
            InlineKeyboardButton("🚀 Yuk Joylash", url="https://t.me/MADIWAYy_bot"),
            InlineKeyboardButton("🏔 MadiWay Kanal", url="https://t.me/MADIWAYy"),
            InlineKeyboardButton("💬 Lichkaga yozish", url=f"tg://user?id={user.id}")
        )

        # 1 dan 6 martagacha yuborish
        for i in range(min(count, 6)):
            await bot.send_message(KANAL_ID, post_text, reply_markup=kb, parse_mode="Markdown")
            if topic_id:
                try:
                    await bot.send_message(GROUP_ID, post_text, reply_markup=kb, message_thread_id=topic_id, parse_mode="Markdown")
                except Exception as e:
                    logging.error(f"Topicga yuborishda xato: {e}")
            await asyncio.sleep(1)

@dp.callback_query_handler(lambda c: c.data == "view_face_db")
async def view_faces(callback: types.CallbackQuery):
    if not face_database:
        await callback.answer("Hozircha Face ID bazasi bo'sh!", show_alert=True)
        return
    await callback.message.answer("📸 **Face ID bazasidagi foydalanuvchilar:**")
    for uid, info in face_database.items():
        await callback.message.answer(f"👤 {info['name']}\n📞 {info['phone']}\n🆔 {uid}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
