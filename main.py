import logging
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)

# --- KONFIGURATSIYA ---
# Yangi API tokeningiz
TOKEN = "8791239714:AAGeDUktKzciq9ftUp4lZZOzIuyItQXv5wM" 
# Ma'lumot tushadigan guruh va kanal ID'lari
GROUP_ID = -1003996104316 
CHANNEL_USER = "@MADIWAYy" 
# Sizning GitHub sahifangiz manzili
WEB_APP_URL = "https://madiway.github.io/madiway-bot/"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    # Kodingizdagi tugma bilan bog'lanish
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
        # Siz yuborgan index.html dagi tg.sendData ichidagi ma'lumotlarni o'qiydi
        res = json.loads(message.web_app_data.data)
        
        # Xabarni chiroyli formatda tayyorlaymiz
        report = (
            f"🚛 **YANGI YUK E'LONI**\n\n"
            f"🌍 **Yo'nalish:** #{res['t_name']}\n"
            f"📦 **Tavsif:** {res['desc']}\n"
            f"⏰ **Vaqt:** {res['time']}\n"
            f"👤 **Mijoz:** {res['u_name']}\n"
            f"📞 **Tel:** {res['u_phone']}\n\n"
            f"🤖 #MadiWay_System"
        )

        # 1. Telegram kanalga yuborish
        await bot.send_message(chat_id=CHANNEL_USER, text=report, parse_mode="Markdown")
        
        # 2. Guruhga (tegishli topic_id bilan) yuborish
        try:
            # res['t_id'] - bu sizning kodingizdagi topics ichidagi id
            await bot.send_message(
                chat_id=GROUP_ID, 
                message_thread_id=res['t_id'], 
                text=report, 
                parse_mode="Markdown"
            )
        except Exception as e:
            # Agar topic topilmasa, oddiy guruh xabari sifatida yuboradi
            logging.warning(f"Topic xatosi: {e}")
            await bot.send_message(chat_id=GROUP_ID, text=report, parse_mode="Markdown")

        await message.answer("✅ Rahmat! Yukingiz kanal va guruhga muvaffaqiyatli e'lon qilindi.")

    except Exception as e:
        logging.error(f"Xatolik yuz berdi: {e}")
        await message.answer("❌ Ma'lumotni yuborishda texnik xatolik yuz berdi.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
