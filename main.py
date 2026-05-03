import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

# Loglar
logging.basicConfig(level=logging.INFO)

# --- SOZLAMALAR ---
TOKEN = "8791239714:AAH17eobRUq3xCUMYJipwcSrmYPJPfZr3Rs"
GROUP_ID = -1003996104316  # Asosiy guruh ID
CHANNEL_USER = "@MADIWAYy" # Kanal username
WEB_APP_URL = "https://yusufxonpro.github.io/madiway/"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    caption = (
        "🏔 **MadiWay Professional v3.0**\n\n"
        "Xush kelibsiz! Tizimga kirish va yuklarni boshqarish uchun pastdagi tugmani bosing.\n\n"
        "🚛 **MadiWay — Yukingiz xavfsiz qo'llarda!**"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Ilovani ochish", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])

    try:
        # madiway_banner.png loyiha papkasida bo'lishi kerak
        photo = FSInputFile("madiway_banner.png")
        await message.answer_photo(photo=photo, caption=caption, reply_markup=keyboard, parse_mode="Markdown")
    except:
        await message.answer(caption, reply_markup=keyboard, parse_mode="Markdown")

@dp.message(F.content_type == types.ContentType.WEB_APP_DATA)
async def handle_webapp_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        
        # HTML dagi action ga qarab tekshiramiz
        if data.get('action') == "auto_bot_yuk":
            report = (
                f"🚛 **YANGI SMART YUK E'LONI**\n\n"
                f"🌍 **Yo'nalish:** {data['topic_name'].upper()}\n"
                f"📝 **Ma'lumot:** {data['msg']}\n"
                f"⏰ **Vaqt:** {data['send_time'] if not data['send_now'] else 'Hozir'}\n"
                f"🔁 **Takrorlash:** {data['repeat']} marta\n\n"
                f"👤 **Yuboruvchi:** {message.from_user.full_name}\n"
                f"🤖 #MadiWay_Smart_Bot"
            )

            # 1. Kanalga yuborish
            await bot.send_message(chat_id=CHANNEL_USER, text=report, parse_mode="Markdown")
            
            # 2. Guruhga yuborish (Topic bo'lsa topicga, bo'lmasa umumiy guruhga)
            try:
                await bot.send_message(
                    chat_id=GROUP_ID, 
                    message_thread_id=data['topic_id'], 
                    text=report, 
                    parse_mode="Markdown"
                )
            except:
                # Agar topic topilmasa, shunchaki guruhga yuboradi
                await bot.send_message(chat_id=GROUP_ID, text=report, parse_mode="Markdown")

            await message.answer("✅ Yukingiz Smart Bot tomonidan kanal va guruhga joylandi!")

    except Exception as e:
        logging.error(f"Xato: {e}")
        await message.answer("❌ Bot ma'lumotni qabul qila olmadi.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
