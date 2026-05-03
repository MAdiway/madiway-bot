import logging
import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

# Bot tokeningiz
TOKEN = "8791239714:AAH17eobRUq3xCUMYJipwcSrmYPJPfZr3Rs"
ADMINS = [6977836294, 8112179116]
KANAL_ID = "@MADIWAYy"
GROUP_ID = -1002345678901 # Guruh ID sini tekshirib o'rnating

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Yo'nalishlar (Topic ID)
TOPICS = {
    "Europe": 2, "Rossiya": 4, "Qirg'iziston": 6, "Kazakistan": 8,
    "Eron": 10, "Tojikston": 12, "Germaniya": 14, "Belarusiya": 16,
    "Gruziya": 18, "Ukraina": 20
}

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    # Oldingi barcha menyu tugmalarini (ReplyKeyboard) o'chirib tashlaymiz
    remove_menu = ReplyKeyboardRemove()
    
    # Yangi Inline tugmalar
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🏔 MadiWay Ilovasi", web_app=WebAppInfo(url="https://madiway.github.io/madiway-bot/"))
    )
    
    if message.from_user.id in ADMINS:
        kb.add(
            InlineKeyboardButton("📸 Face ID Bazasi", callback_data="view_faces"),
            InlineKeyboardButton("💬 Chat Monitoring", callback_data="chat_monitor")
        )

    # Eski fura banneri - Start uchun
    banner_url = "https://madiway.github.io/madiway-bot/truck_transparent.png"
    caption = (
        "🚛 **MADIWAY Logistics**\n\n"
        "Xush kelibsiz! Ilovaga kirish uchun pastdagi tugmani bosing.\n"
        "Barcha menyular tozalandi, endi faqat ilova orqali ishlaymiz."
    )
    
    # Avval menyuni tozalab, keyin xabarni yuboramiz
    await message.answer("Menyular yangilanmoqda...", reply_markup=remove_menu)
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
        
        kb = InlineKeyboardMarkup().add(
            InlineKeyboardButton("📞 Aloqa", url=f"tg://user?id={user.id}"),
            InlineKeyboardButton("🚀 Yuk Joylash", url="https://t.me/MADIWAYy_bot")
        )

        # Takrorlash soni (1-6)
        count = int(data.get("repeat", 1))
        for _ in range(min(count, 6)):
            await bot.send_message(KANAL_ID, post_text, reply_markup=kb, parse_mode="Markdown")
            if topic_id:
                await bot.send_message(GROUP_ID, post_text, reply_markup=kb, message_thread_id=topic_id, parse_mode="Markdown")
            await asyncio.sleep(1)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
