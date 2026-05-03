import asyncio
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart

TOKEN = "7299092416:AAFTYm1L_5y7X-m2yU6nK-35wYFjK5W5yA8"
# DIQQAT: Guruhingiz ID sini tekshirib oling!
GROUP_ID = -1002444342416 

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def welcome(message: types.Message):
    kb = [[types.KeyboardButton(text="🚛 MadiWay Ilovasi", web_app=types.WebAppInfo(url="ILOVANGIZ_LINKI"))]]
    markup = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("MadiWay Pro v10 tizimiga xush kelibsiz! Ilovadan foydalanish uchun tugmani bosing.", reply_markup=markup)

@dp.message(F.content_type == types.ContentType.WEB_APP_DATA)
async def web_app_handler(message: types.Message):
    data = json.loads(message.web_app_data.data)
    
    if data['action'] == "post_yuk":
        report = (
            f"📦 **YANGI YUK BILDIRNOMASI**\n\n"
            f"👤 **Mijoz:** {data['user']}\n"
            f"📞 **Telefon:** {data['phone']}\n"
            f"🚛 **Yuk:** {data['text']}\n"
            f"⏰ **Vaqt:** {data['time']}\n"
            f"🆔 **Topic ID:** {data['topic_id']}"
        )
        
        try:
            # Yukni aynan o'sha viloyat/davlat topiciga yuboradi
            await bot.send_message(
                chat_id=GROUP_ID,
                message_thread_id=data['topic_id'],
                text=report,
                parse_mode="Markdown"
            )
            await message.answer("✅ Yukingiz guruhga muvaffaqiyatli yuborildi!")
        except Exception as e:
            await message.answer(f"❌ Xatolik: Guruhdagi Topic ID ({data['topic_id']}) bilan bog'lanib bo'lmadi.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
