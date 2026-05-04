import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

# --- SOZLAMALAR ---
BOT_TOKEN = "8724439262:AAFGNuQQ4IxdqitlcCEtkHLsvyFwSPg_b1c"
# Sening kodingdagi IDlar
GROUP_ID = -1002441995574  # Guruh ID (integer formatda)
CHANNEL_ID = "@MADIWAYy"    # Kanal username yoki ID

# Loggingni sozlash
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 1. Bot ishga tushganda xabar berish
async def on_startup():
    print("MadiWay Logistics boti ishga tushdi!")
    try:
        # Admin topicga bot yoqilgani haqida yozish
        await bot.send_message(
            chat_id=GROUP_ID,
            text="🚀 <b>MadiWay Logistcs Tizimi ishga tushdi!</b>\nWeb App orqali buyurtmalarni qabul qilishga tayyor.",
            parse_mode=ParseMode.HTML,
            message_thread_id=1 # Admin topic ID
        )
    except Exception as e:
        print(f"Xatolik: {e}")

# 2. Botga /start buyrug'i berilganda (Web Appni ochish uchun tugma)
@dp.message(lambda message: message.text == "/start")
async def start_cmd(message: types.Message):
    # Web App ochish tugmasini yaratish
    web_app = types.WebAppInfo(url="https://YOUR-URL.com") # O'zingning hosting manzilingni qo'y
    kb = [
        [types.KeyboardButton(text="🚚 Yuk yuborish", web_app=web_app)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    
    await message.answer(
        f"Assalomu alaykum {message.from_user.full_name}!\n<b>MadiWay Logistics</b> tizimiga xush kelibsiz.\n\nPastdagi tugmani bosing va yuklarni e'lon qiling.",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

async def main():
    await on_startup()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi")
