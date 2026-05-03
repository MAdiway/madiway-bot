import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# Loglarni Railway-da kuzatish uchun
logging.basicConfig(level=logging.INFO)

# --- KONFIGURATSIYA ---
TOKEN = "8791239714:AAH17eobRUq3xCUMYJipwcSrmYPJPfZr3Rs"
GROUP_ID = -1003996104316
CHANNEL_USER = "@MADIWAYy"
WEB_APP_URL = "https://yusufxonpro.github.io/madiway/" # Ilovangiz linki
BANNER_URL = "https://i.postimg.cc/WbcqK7FF/daf-xf-daf-trucks-car-renault-magnum-car-removebg-preview.png"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # Siz xohlagan banner matni
    caption = (
        "🏔 **MadiWay | Global Logistics & Dispatch 🚀**\n\n"
        "Xalqaro yuk tashish va professional dispetcherlik xizmatlari tarmog'iga xush kelibsiz! "
        "Biz to'rtta davlatni yagona xavfsiz marshrut bilan bog'laymiz:\n\n"
        "🌍 **Bizning yo'nalishlar:**\n"
        "📍 O'zbekiston 🇺🇿\n"
        "📍 Qozog'iston 🇰🇿\n"
        "📍 Rossiya 🇷🇺\n"
        "📍 Ozarbayjon 🇦🇿\n\n"
        "🛡 **Nega aynan MadiWay?**\n"
        "✅ Ishonchlilik: Yukingiz manzili va vaqti bizning nazoratimizda.\n"
        "✅ Tezkorlik: Eng qulay va xavfsiz yo'llarni taqdim etamiz.\n"
        "✅ Professional Dispetcherlik: 24/7 aloqa va harakat nazorati.\n\n"
        "🚛 **MadiWay — Sizning yukingiz, bizning mas'uliyatimiz!**\n\n"
        "📥 Bog'lanish uchun: @Madiways\n"
        "📢 Kanal: T.me/MADIWAYy\n"
        "💬 Guruh: @MADIWAY_Gr"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏔 MadiWay Ilovasi", web_app=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton(text="📢 Kanal", url="https://t.me/MADIWAYy")],
        [InlineKeyboardButton(text="💬 Guruh", url="https://t.me/MADIWAY_Gr")]
    ])

    await message.answer_photo(
        photo=BANNER_URL,
        caption=caption,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@dp.message(F.content_type == types.ContentType.WEB_APP_DATA)
async def handle_webapp_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        target = data.get('target')
        
        report = (
            f"🚛 **YANGI YUK BILDIRNOMASI**\n\n"
            f"📍 **Yo'nalish:** {data['t_name']}\n"
            f"📦 **Yuk:** {data['desc']}\n"
            f"⏰ **Vaqt:** {data['time']}\n"
            f"👤 **Mijoz:** {data['u_name']}\n"
            f"📞 **Telefon:** {data['u_phone']}\n\n"
            f"🤖 #MadiWay_System_v15"
        )

        if target == 'group':
            # Guruh mavzusiga yuborish
            await bot.send_message(
                chat_id=GROUP_ID,
                message_thread_id=data['t_id'],
                text=report,
                parse_mode="Markdown"
            )
            await message.answer(f"✅ Yuk muvaffaqiyatli **Guruhning {data['t_name']} bo'limiga** yuborildi!")
        else:
            # Kanalga yuborish
            await bot.send_message(
                chat_id=CHANNEL_USER,
                text=report,
                parse_mode="Markdown"
            )
            await message.answer("✅ Yuk muvaffaqiyatli **Kanalga** yuborildi!")

    except Exception as e:
        logging.error(f"Xato: {e}")
        await message.answer("❌ Ma'lumotni yuborishda xatolik yuz berdi.")

async def main():
    # Eski so'rovlarni o'chirib, pollingni boshlash
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
