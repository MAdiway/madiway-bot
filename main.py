import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

# Railway loglari uchun
logging.basicConfig(level=logging.INFO)

TOKEN = "7299092416:AAFTYm1L_5y7X-m2yU6nK-35wYFjK5W5yA8"
GROUP_ID = -1003996104316
CHANNEL_USER = "@MADIWAYy"
# Ilovangiz manzili (Railway yoki GitHub Pages linki)
WEB_APP_URL = "https://yusufxonpro.github.io/madiway/" 

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # Banner rasmini yuborish va ilovani ochish tugmasi
    # Eslatma: madiway_banner.png fayli bot bilan birga loyiha papkasida bo'lishi kerak
    try:
        banner = FSInputFile("madiway_banner.png")
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏔 MadiWay Ilovasi", web_app=WebAppInfo(url=WEB_APP_URL))]
        ])
        
        await message.answer_photo(
            photo=banner,
            caption=f"Assalomu alaykum, {message.from_user.full_name}!\n\n"
                    f"🚛 **MadiWay** — professional logistika tizimiga xush kelibsiz.\n"
                    f"Yukingizni guruh yoki kanalga yuborish uchun pastdagi tugmani bosing.",
            reply_markup=keyboard
        )
    except Exception as e:
        # Agar rasm topilmasa, matnning o'zini yuboradi
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏔 MadiWay Ilovasi", web_app=WebAppInfo(url=WEB_APP_URL))]
        ])
        await message.answer(
            "🚛 **MadiWay** tizimi ishga tushdi. Ilovani ochish uchun tugmani bosing:",
            reply_markup=keyboard
        )

@dp.message(F.content_type == types.ContentType.WEB_APP_DATA)
async def handle_webapp_data(message: types.Message):
    try:
        res = json.loads(message.web_app_data.data)
        target = res['target']
        
        msg_text = (
            f"🚛 **YANGI YUK E'LONI**\n\n"
            f"📍 **Yo'nalish:** {res['t_name']}\n"
            f"📦 **Yuk:** {res['desc']}\n"
            f"⏰ **Vaqt:** {res['time']}\n"
            f"👤 **Mijoz:** {res['u_name']}\n"
            f"📞 **Telefon:** {res['u_phone']}\n\n"
            f"🤖 #MadiWay Pro v15.2"
        )

        if target == 'group':
            # Guruh mavzusiga (Topic)
            await bot.send_message(
                chat_id=GROUP_ID,
                message_thread_id=res['t_id'],
                text=msg_text,
                parse_mode="Markdown"
            )
            await message.answer(f"✅ Yuk muvaffaqiyatli guruhning **{res['t_name']}** bo'limiga yuborildi!")
        else:
            # Kanalga
            await bot.send_message(
                chat_id=CHANNEL_USER,
                text=msg_text,
                parse_mode="Markdown"
            )
            await message.answer("✅ Yuk muvaffaqiyatli **Kanalga** yuborildi!")

    except Exception as e:
        logging.error(f"Xato: {e}")
        await message.answer(f"❌ Xatolik: {str(e)}")

async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
