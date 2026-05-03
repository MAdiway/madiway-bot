import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# Loglarni yoqish (xatolarni ko'rib turish uchun)
logging.basicConfig(level=logging.INFO)

# --- SOZLAMALAR ---
TOKEN = "8791239714:AAH17eobRUq3xCUMYJipwcSrmYPJPfZr3Rs"
GROUP_ID = -1003996104316 
CHANNEL_USER = "@MADIWAYy" 
WEB_APP_URL = "https://yusufxonpro.github.io/madiway/"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# /start buyrug'i berilganda
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # Katta tugma (Reply Keyboard) yaratish
    # Bu usulda ma'lumot botga 100% o'tadi
    kb = [
        [KeyboardButton(text="🚛 Yuk yuborish", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb, 
        resize_keyboard=True, 
        one_time_keyboard=False,
        input_field_placeholder="Yuk yuborish uchun pastdagi tugmani bosing"
    )
    
    await message.answer(
        "🏔 **MadiWay Logistics tizimiga xush kelibsiz!**\n\n"
        "Yuk joylashtirish uchun pastdagi **'🚛 Yuk yuborish'** tugmasini bosing.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# Web App'dan ma'lumot kelganini ushlash
@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    try:
        # JSON formatidagi ma'lumotni lug'atga aylantiramiz
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

        # 1. Kanalga yuborish
        await bot.send_message(chat_id=CHANNEL_USER, text=report, parse_mode="Markdown")
        
        # 2. Guruhning tegishli yo'nalishiga (topic) yuborish
        try:
            await bot.send_message(
                chat_id=GROUP_ID, 
                message_thread_id=res['t_id'], 
                text=report, 
                parse_mode="Markdown"
            )
        except Exception as topic_err:
            # Agar topic_id topilmasa, shunchaki guruhning o'ziga yuboradi
            await bot.send_message(chat_id=GROUP_ID, text=report, parse_mode="Markdown")

        await message.answer("✅ Rahmat! Ma'lumotlaringiz qabul qilindi va e'lon qilindi.")

    except Exception as e:
        logging.error(f"Xato: {e}")
        await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

# Botni ishga tushirish funksiyasi
async def main():
    # Kichkina ko'k Menu tugmasini o'chirish (default holatga qaytarish)
    # Bu rasmda ko'ringan muammoni hal qiladi
    await bot.set_chat_menu_button(menu_button=types.MenuButtonDefault())
    
    # Eskidan qolib ketgan so'rovlarni tozalash
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Botni ishga tushirish
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi")
