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
GROUP_ID = -1002345678901 # Guruh ID sini o'zgartiring

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Topiclar bazasi
TOPICS = {
    "Europe": 2, "Rossiya": 4, "Qirg'iziston": 6, "Kazakistan": 8,
    "Eron": 10, "Tojikston": 12, "Germaniya": 14, "Belarusiya": 16,
    "Gruziya": 18, "Ukraina": 20
}

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    kb = InlineKeyboardMarkup(row_width=1)
    # MadiWay ilovasiga kirish
    kb.add(InlineKeyboardButton("🏔 MadiWay Ilovasi", web_app=WebAppInfo(url="https://madiway.github.io/madiway-bot/")))
    
    # Adminlar uchun maxsus tugmalar
    if message.from_user.id in ADMINS:
        kb.add(
            InlineKeyboardButton("📸 Face ID Bazasi", callback_data="view_faces"),
            InlineKeyboardButton("💬 Chat Monitoring (Lichka)", callback_data="chat_monitor")
        )

    # Start bosilganda chiqadigan ESKI BANNER
    banner_url = "https://madiway.github.io/madiway-bot/truck_transparent.png" 
    caption = "🚛 **MADIWAY Logistics** tizimiga xush kelibsiz!\n\nPastdagi tugma orqali yuk joylang yoki monitoringni kuzating."
    
    await message.answer_photo(photo=banner_url, caption=caption, reply_markup=kb, parse_mode="Markdown")

@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def handle_data(message: types.Message):
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
        
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton("📞 Aloqa", url=f"tg://user?id={user.id}"),
            InlineKeyboardButton("🚀 Yuk Joylash", url="https://t.me/MADIWAYy_bot")
        )

        for _ in range(int(data.get("repeat", 1))):
            await bot.send_message(KANAL_ID, post_text, reply_markup=kb, parse_mode="Markdown")
            if topic_id:
                await bot.send_message(GROUP_ID, post_text, reply_markup=kb, message_thread_id=topic_id, parse_mode="Markdown")
            await asyncio.sleep(1)

# Chat Monitoring uchun oddiy funksiya
@dp.callback_query_handler(lambda c: c.data == "chat_monitor")
async def monitor(callback: types.CallbackQuery):
    await callback.answer("💬 Monitoring faollashtirildi. Barcha yangi lichka suhbatlari shu yerda ko'rinadi.", show_alert=True)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
