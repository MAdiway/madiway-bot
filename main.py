import logging
import json
import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# --- KONFIGURATSIYA ---
TOKEN = "8724439262:AAFGNuQQ4IxdqitlcCEtkHLsvyFwSPg_b1c"
GROUP_ID = -1003996104316
CHANNEL_ID = "@MADIWAYy"
BANNER_URL = "https://raw.githubusercontent.com/madiway/madiway-bot/main/madiway_banner.png"
WEB_APP_URL = "https://madiway.github.io/madiway-bot/"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

BAD_WORDS = ["jalab", "qo'toq", "am", "iflos", "yaramas", "dalbayob", "gandon"]

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="🚛 MadiWay Ilovasi", web_app=WebAppInfo(url=WEB_APP_URL))
    )
    
    caption = (
        "<b>🏔 MadiWay | Global Logistics 🚀</b>\n\n"
        "Xalqaro yuk tashish tizimiga xush kelibsiz!\n\n"
        "Pastdagi tugmani bosing va Face ID orqali tizimga kiring.\n\n"
        "📢 Kanal: T.me/MADIWAYy\n"
        "👥 Guruh: @MADIWAY_Gr"
    )
    
    try:
        await bot.send_photo(message.chat.id, photo=BANNER_URL, caption=caption, reply_markup=kb, parse_mode="HTML")
    except Exception as e:
        logging.error(f"Start xatosi: {e}")
        await message.answer(caption, reply_markup=kb, parse_mode="HTML")

@dp.message_handler(content_types=['web_app_data'])
async def web_app_data_handler(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        now = datetime.datetime.now().strftime("%d.%m.%Y | %H:%M")
        
        text = (
            f"🚛 <b>YANGI YUK E'LONI</b>\n"
            f"━━━━━━━━━━━━━━\n"
            f"📍 <b>Yo'nalish:</b> #{data.get('t_name', 'Noma'lum')}\n"
            f"📦 <b>Yuk:</b> {data.get('desc', 'Tavsif yo'q')}\n"
            f"⏰ <b>Vaqt:</b> {data.get('time', 'Hozir')}\n"
            f"━━━━━━━━━━━━━━\n"
            f"👤 <b>Yuboruvchi:</b> {data.get('u_name', 'Mijoz')}\n"
            f"📞 <b>Tel:</b> {data.get('u_phone', 'Noma'lum')}\n"
            f"📅 <b>Sana:</b> {now}"
        )

        kb = InlineKeyboardMarkup().add(
            InlineKeyboardButton("💬 Bog'lanish", url=f"tg://user?id={message.from_user.id}")
        )

        await bot.send_message(CHANNEL_ID, text, reply_markup=kb, parse_mode="HTML")
        await bot.send_message(GROUP_ID, text, reply_markup=kb, parse_mode="HTML")
        await message.answer("✅ E'loningiz qabul qilindi!")
    except Exception as e:
        logging.error(f"Data xatosi: {e}")

@dp.message_handler(chat_id=GROUP_ID)
async def cleaner(message: types.Message):
    if not message.text: return
    txt = message.text.lower()
    if any(word in txt for word in BAD_WORDS):
        try: await message.delete()
        except: pass

if __name__ == "__main__":
    # skip_updates=True eski "conflict"larni tozalaydi
    executor.start_polling(dp, skip_updates=True)
