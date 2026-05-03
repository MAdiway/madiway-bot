import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, MenuButtonDefault

# Loglarni yoqish
logging.basicConfig(level=logging.INFO)

# --- KONFIGURATSIYA ---
TOKEN = "8791239714:AAGW7AEy6Zh3Rtz164oJex_MWEsLx2ROBM4"
GROUP_ID = -1003996104316 
CHANNEL_USER = "@MADIWAYy" 
WEB_APP_URL = "https://madiway.github.io/madiway-bot/" # GitHub linkinigiz

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # Pastdagi ko'k 'Menu' tugmasi o'rniga ishlaydigan katta tugma
    kb = [
        [KeyboardButton(text="🚛 Yuk yuborish", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb, 
        resize_keyboard=True,
        input_field_placeholder="Yuk yuborish uchun pastdagi tugmani bosing"
    )
    
    await message.answer(
        "🏔 **MadiWay Logistics tizimiga xush kelibsiz!**\n\n"
        "Yuk joylashtirish uchun pastdagi **'🚛 Yuk yuborish'** tugmasini bosing.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    try:
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
        
        # Guruhga yuborish
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
        await message.answer("❌ Xatolik yuz berdi. Qayta urinib ko'ring.")

async def main():
    # Bot yonganda eski ko'k menyu tugmasini API orqali yo'qotadi
    await bot.set_chat_menu_button(chat_id=None, menu_button=MenuButtonDefault())
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
