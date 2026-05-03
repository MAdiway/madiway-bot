import logging
import json
import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# --- SOZLAMALAR ---
TOKEN = "8724439262:AAFGNuQQ4IxdqitlcCEtkHLsvyFwSPg_b1c"
GROUP_ID = -1003996104316  # Guruh ID
CHANNEL_ID = "@MADIWAYy"    # Kanal ID
BANNER_URL = "https://raw.githubusercontent.com/madiway/madiway-bot/main/madiway_banner.png"
WEB_APP_URL = "https://madiway.github.io/madiway-bot/"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="🚛 MadiWay Ilovasi", web_app=WebAppInfo(url=WEB_APP_URL))
    )
    caption = (
        "<b>🏔 MadiWay | Global Logistics 🚀</b>\n\n"
        "Xalqaro yuk tashish tizimiga xush kelibsiz!\n\n"
        "Pastdagi tugmani bosing va ilova orqali yuk e'lonini yuboring."
    )
    # HTML formatda rasm yuborish
    await bot.send_photo(message.chat.id, photo=BANNER_URL, caption=caption, reply_markup=kb, parse_mode="HTML")

@dp.message_handler(content_types=['web_app_data'])
async def web_app_data_handler(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        now = datetime.datetime.now().strftime("%d.%m.%Y | %H:%M")
        
        # Xabar matni (Faqat HTML)
        text = (
            f"🚛 <b>YANGI YUK E'LONI</b>\n"
            f"━━━━━━━━━━━━━━\n"
            f"📍 <b>Yo'nalish:</b> #{data.get('t_name', 'Nomaʼlum')}\n"
            f"📦 <b>Yuk:</b> {data.get('desc', 'Tavsif yoʻq')}\n"
            f"⏰ <b>Vaqt:</b> {data.get('time', 'Hozir')}\n"
            f"━━━━━━━━━━━━━━\n"
            f"👤 <b>Yuboruvchi:</b> {data.get('u_name', 'Mijoz')}\n"
            f"📞 <b>Tel:</b> {data.get('u_phone', 'Nomaʼlum')}\n"
            f"📅 <b>Sana:</b> {now}"
        )

        # 1. KANALGA YUBORISH
        await bot.send_message(CHANNEL_ID, text, parse_mode="HTML")

        # 2. GURUHGA (TOPICGA) YUBORISH
        topic_id = data.get('t_id') # Ilovadan kelayotgan Topic (Mavzu) ID si
        try:
            await bot.send_message(GROUP_ID, text, message_thread_id=topic_id, parse_mode="HTML")
        except:
            # Agar topic_id xato bo'lsa, oddiy guruhga yuboradi
            await bot.send_message(GROUP_ID, text, parse_mode="HTML")

        await message.answer("✅ E'loningiz muvaffaqiyatli yuborildi!")

    except Exception as e:
        logging.error(f"Xato yuz berdi: {e}")
        await message.answer("❌ Xatolik: Ma'lumotni qayta ishlashda muammo bo'ldi.")

if __name__ == "__main__":
    # skip_updates=True eski xabarlarni o'chirib yuboradi (Conflict-ni oldini oladi)
    executor.start_polling(dp, skip_updates=True)
