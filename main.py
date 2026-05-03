import logging
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)

# --- KONFIGURATSIYA ---
TOKEN = "8791239714:AAGeDUktKzciq9ftUp4lZZOzIuyItQXv5wM" # Yangi tokeningiz
GROUP_ID = -1003996104316 
CHANNEL_USER = "@MADIWAYy" 
WEB_APP_URL = "https://madiway.github.io/madiway-bot/"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    # Pastdagi asosiy tugmani yaratish
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(text="🚛 Yuk yuborish", web_app=WebAppInfo(url=WEB_APP_URL)))
    
    await message.answer(
        "🏔 **MadiWay Logistics tizimiga xush kelibsiz!**\n\n"
        "Yuk joylashtirish uchun pastdagi tugmani bosing.",
        reply_markup=kb,
        parse_mode="Markdown"
    )

@dp.message_handler(content_types=['web_app_data'])
async def handle_webapp_data(message: types.Message):
    try:
        # WebApp'dan kelgan JSON ma'lumotni o'qiymiz
        res = json.loads(message.web_app_data.data)
        
        report = (
            f"🚛 **YANGI YUK E'LONI**\n\n"
            f"🌍 **Yo'nalish:** #{res['t_name']}\n"
            f"📦 **Tavsif:** {res['desc']}\n"
            f"⏰ **Vaqt:** {res['time']}\n"
            f"👤 **Mijoz:** {res['u_name']}\n"
            f"📞 **Tel:** {res['u_phone']}\n\n"
            f"🤖 #MadiWay_System"
        )

        # Kanalga yuborish
        await bot.send_message(chat_id=CHANNEL_USER, text=report, parse_mode="Markdown")
        
        # Guruhga (topic_id bilan) yuborish
        try:
            await bot.send_message(
                chat_id=GROUP_ID, 
                message_thread_id=res['t_id'], 
                text=report, 
                parse_mode="Markdown"
            )
        except:
            await bot.send_message(chat_id=GROUP_ID, text=report, parse_mode="Markdown")

        await message.answer("✅ Rahmat! Yukingiz kanal va guruhga e'lon qilindi.")

    except Exception as e:
        logging.error(f"Xato: {e}")
        await message.answer("❌ Ma'lumot yuborishda xatolik yuz berdi.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
