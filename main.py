import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)

# --- KONFIGURATSIYA ---
TOKEN = "8791239714:AAH17eobRUq3xCUMYJipwcSrmYPJPfZr3Rs"
GROUP_ID = -1003996104316
CHANNEL_USER = "@MADIWAYy"
WEB_APP_URL = "https://yusufxonpro.github.io/madiway/" # GitHub Pages manzilingiz

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # Banner matni
    caption = (
        "🏔 **MadiWay | Global Logistics & Dispatch 🚀**\n\n"
        "Xalqaro yuk tashish va professional dispetcherlik xizmatlari tarmog'iga xush kelibsiz!\n\n"
        "🌍 **Bizning yo'nalishlar:**\n"
        "📍 O'zbekiston 🇺🇿, Qozog'iston 🇰🇿, Rossiya 🇷🇺, Ozarbayjon 🇦🇿\n\n"
        "🛡 **Nega aynan MadiWay?**\n"
        "✅ Ishonchlilik, Tezkorlik va Professional nazorat.\n\n"
        "🚛 **MadiWay — Sizning yukingiz, bizning mas'uliyatimiz!**\n\n"
        "📢 Kanal: T.me/MADIWAYy\n"
        "💬 Guruh: @MADIWAY_Gr"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏔 Ilovani ochish", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])

    try:
        # Fayl tizimidan madiway_banner.png ni yuklash
        photo = FSInputFile("madiway_banner.png")
        await message.answer_photo(photo=photo, caption=caption, reply_markup=keyboard, parse_mode="Markdown")
    except:
        # Agar rasm topilmasa, matnni o'zini yuboradi
        await message.answer(caption, reply_markup=keyboard, parse_mode="Markdown")

@dp.message(F.content_type == types.ContentType.WEB_APP_DATA)
async def handle_webapp_data(message: types.Message):
    try:
        # WebApp'dan kelgan ma'lumotni o'qish
        data = json.loads(message.web_app_data.data)
        
        report = (
            f"🚛 **YANGI YUK E'LONI**\n\n"
            f"📍 **Yo'nalish:** {data['t_name']}\n"
            f"📦 **Yuk:** {data['desc']}\n"
            f"⏰ **Vaqt:** {data['time']}\n"
            f"👤 **Mijoz:** {data['u_name']}\n"
            f"📞 **Telefon:** {data['u_phone']}\n\n"
            f"🤖 #MadiWay_System"
        )

        # 1. Guruhdagi tegishli Topicga yuborish
        await bot.send_message(
            chat_id=GROUP_ID,
            message_thread_id=data['t_id'],
            text=report,
            parse_mode="Markdown"
        )

        # 2. Kanalga yuborish
        await bot.send_message(
            chat_id=CHANNEL_USER,
            text=report,
            parse_mode="Markdown"
        )

        await message.answer("✅ Yuk muvaffaqiyatli kanal va guruhga yuborildi!")

    except Exception as e:
        logging.error(f"Xato: {e}")
        await message.answer(f"❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
