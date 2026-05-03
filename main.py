import logging
import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

# Bot sozlamalari
TOKEN = "8791239714:AAH17eobRUq3xCUMYJipwcSrmYPJPfZr3Rs"
ADMINS = [6977836294, 8112179116]
KANAL_ID = "@MADIWAYy"
GROUP_ID = -1002345678901 # O'zingizning guruh ID-ingizni qo'ying

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# GitHub'dagi asosiy start banneri
START_BANNER = "https://raw.githubusercontent.com/madiway/madiway-bot/main/madiway_banner.png"

# Barcha 10 ta topic
TOPICS = {
    "Europe": 2, "Rossiya": 4, "Qirg'iziston": 6, "Kazakistan": 8, "Eron": 10,
    "Tojikston": 12, "Germaniya": 14, "Belarusiya": 16, "Gruziya": 18, "Ukraina": 20
}

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    # Oldingi menyularni tozalash
    remove_kb = ReplyKeyboardRemove()
    
    # Ilova tugmasi
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("🏔 MadiWay Ilovasi", web_app=WebAppInfo(url="https://madiway.github.io/madiway-bot/")))
    
    # Adminlar uchun qo'shimcha tugmalar (faqat bitta xabar ichida)
    if message.from_user.id in ADMINS:
        kb.add(
            InlineKeyboardButton("📸 Face ID Bazasi", callback_data="view_faces"),
            InlineKeyboardButton("💬 Chat Monitoring", callback_data="chat_monitor")
        )

    caption = (
        "🚛 **MADIWAY | Professional Logistics**\n\n"
        "Xalqaro yuk tashish tizimiga xush kelibsiz!\n"
        "Pastdagi tugma orqali ilovani oching."
    )
    
    # Hammasi bitta xabarda keladi
    await message.answer_photo(photo=START_BANNER, caption=caption, reply_markup=kb, parse_mode="Markdown")

@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def handle_webapp_data(message: types.Message):
    data = json.loads(message.web_app_data.data)
    user = message.from_user

    if data.get("action") == "post":
        topic_id = TOPICS.get(data['country'])
        post_text = (
            f"🚛 **#YANGI_YUK | {data['country']}**\n\n"
            f"📦 **Yuk:** {data['content']}\n"
            f"⏰ **Vaqt:** {data['time']}\n"
            f"👤 **E'lon:** {user.full_name}\n"
            f"🏁 @MADIWAYy"
        )
        
        kb = InlineKeyboardMarkup().add(
            InlineKeyboardButton("📞 Aloqa", url=f"tg://user?id={user.id}"),
            InlineKeyboardButton("🚀 Yuk Joylash", url="https://t.me/MADIWAYy_bot")
        )

        # Takroriy yuborish
        for _ in range(int(data.get("repeat", 1))):
            await bot.send_message(KANAL_ID, post_text, reply_markup=kb, parse_mode="Markdown")
            if topic_id:
                await bot.send_message(GROUP_ID, post_text, reply_markup=kb, message_thread_id=topic_id, parse_mode="Markdown")
            await asyncio.sleep(1)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
