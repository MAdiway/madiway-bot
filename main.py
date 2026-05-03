import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

logging.basicConfig(level=logging.INFO)

# --- SOZLAMALAR ---
TOKEN = "8791239714:AAH17eobRUq3xCUMYJipwcSrmYPJPfZr3Rs"
GROUP_ID = -1003996104316 
CHANNEL_USER = "@MADIWAYy" 
WEB_APP_URL = "https://yusufxonpro.github.io/madiway/"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    caption = (
        "🏔 **MadiWay Logistics v3.5**\n\n"
        "Yuk yuborish uchun pastdagi tugmani bosing va kerakli yo'nalishni tanlang."
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚛 Yuk yuborish", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])
    try:
        photo = FSInputFile("madiway_banner.png")
        await message.answer_photo(photo=photo, caption=caption, reply_markup=keyboard, parse_mode="Markdown")
    except:
        await message.answer(caption, reply_markup=keyboard, parse_mode="Markdown")

@dp.message(F.content_type == types.ContentType.WEB_APP_DATA)
async def handle_webapp_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        
        report = (
            f"🚛 **YANGI YUK E'LONI**\n\n"
            f"🌍 **Yo'nalish:** #{data['t_name']}\n"
            f"📦 **Tavsif:** {data['desc']}\n"
            f"⏰ **Vaqt:** {data['time']}\n"
            f"👤 **Mijoz:** {data['u_name']}\n"
            f"📞 **Tel:** {data['u_phone']}\n\n"
            f"🤖 #MadiWay_System"
        )

        # 1. Kanalga yuborish
        await bot.send_message(chat_id=CHANNEL_USER, text=report, parse_mode="Markdown")
        
        # 2. Guruhdagi Topicga yuborish
        try:
            await bot.send_message(
                chat_id=GROUP_ID, 
                message_thread_id=data['t_id'], 
                text=report, 
                parse_mode="Markdown"
            )
        except:
            await bot.send_message(chat_id=GROUP_ID, text=report, parse_mode="Markdown")

        await message.answer("✅ Yukingiz muvaffaqiyatli joylashtirildi!")

    except Exception as e:
        logging.error(f"Xato: {e}")
        await message.answer("❌ Xatolik: Ma'lumot yuborilmadi.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
