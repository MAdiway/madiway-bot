import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

TOKEN = "8724439262:AAFGNuQQ4IxdqitlcCEtkHLsvyFwSPg_b1c"
BANNER_URL = "https://raw.githubusercontent.com/madiway/madiway-bot/main/madiway_banner.png"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="🚛 MadiWay Ilovasi", web_app=WebAppInfo(url="https://madiway.github.io/madiway-bot/"))
    )
    
    # MUHIM: Faqat HTML formatidan foydalanamiz!
    caption = (
        "<b>🏔 MadiWay | Global Logistics 🚀</b>\n\n"
        "Xalqaro yuk tashish tizimiga xush kelibsiz!\n\n"
        "Pastdagi tugmani bosing va Face ID orqali tizimga kiring."
    )
    
    try:
        # Bu yerda Markdown emas, HTML deb yozilganiga ishonch hosil qiling
        await bot.send_photo(
            message.chat.id, 
            photo=BANNER_URL, 
            caption=caption, 
            reply_markup=kb, 
            parse_mode="HTML"
        )
    except Exception as e:
        logging.error(f"Xato yuz berdi: {e}")
        await message.answer(caption, reply_markup=kb, parse_mode="HTML")

if __name__ == "__main__":
    # skip_updates=True boshqa joydagi botni o'chirib qo'yadi
    executor.start_polling(dp, skip_updates=True)
