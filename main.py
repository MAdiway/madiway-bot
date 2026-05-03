import logging
import json
import datetime
import asyncio
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

BAD_WORDS = ["jalab", "qo'toq", "am", "qotoq", "iflos", "yaramas", "dalbayob", "axmoq", "gandon", "pider"]

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="🚛 MadiWay Ilovasi", web_app=WebAppInfo(url=WEB_APP_URL))
    )
    
    # Markdown o'rniga oddiy matn, xato bermasligi uchun
    caption = (
        "🏔 <b>MadiWay | Global Logistics</b> 🚀\n\n"
        "Xalqaro yuk tashish tizimiga xush kelibsiz!\n\n"
        "Pastdagi tugmani bosing va Face ID orqali tizimga kiring.\n\n"
        "📢 Kanal: T.me/MADIWAYy\n"
        "👥 Guruh: @MADIWAY_Gr"
    )
    
    try:
        # parse_mode="HTML" qildik, bu xavfsizroq
        await bot.send_photo(message.chat.id, photo=BANNER_URL, caption=caption, reply_markup=kb, parse_mode="HTML")
    except Exception as e:
        logging.error(f"Xato: {e}")
        await message.answer(caption, reply_markup=kb, parse_mode="HTML")

@dp.message_handler(content_types=['web_app_data'])
async def web_app_data_handler(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        now = datetime.datetime.now().strftime("%d.%m.%Y | %H:%M")
        
        # Ma'lumotlarni xavfsiz yig'ish
        t_name = str(data.get('t_name', 'Noma\'lum')).replace('<', '&lt;')
        desc = str(data.get('desc', 'Tavsif yo\'q')).replace('<', '&lt;')
        u_name = str(data.get('u_name', 'Mijoz')).replace('<', '&lt;')
        u_phone = str(data.get('u_phone', 'Noma\'lum')).replace('<', '&lt;')

        text = (
            f"🚛 <b>YANGI YUK E'LONI</b>\n"
            f"━━━━━━━━━━━━━━\n"
            f"📍 <b>Yo'nalish:</b> #{t_name}\n"
            f"📦 <b>Yuk:</b> {desc}\n"
            f"⏰ <b>Vaqt:</b> {data.get('time', 'Hozir')}\n"
            f"━━━━━━━━━━━━━━\n"
            f"👤 <b>Yuboruvchi:</b> {u_name}\n"
            f"📞 <b>Tel:</b> {u_phone}\n"
            f"📅 <b>Sana:</b> {now}"
        )

        kb = InlineKeyboardMarkup().add(
            InlineKeyboardButton("💬 Bog'lanish", url=f"tg://user?id={message.from_user.id}")
        )

        await bot.send_message(CHANNEL_ID, text, reply_markup=kb, parse_mode="HTML")
        try:
            # Topic ID xato bo'lsa ham bot to'xtab qolmaydi
            topic_id = data.get('t_id')
            await bot.send_message(GROUP_ID, text, message_thread_id=topic_id, reply_markup=kb, parse_mode="HTML")
        except:
            await bot.send_message(GROUP_ID, text, reply_markup=kb, parse_mode="HTML")

        await message.answer("✅ E'loningiz qabul qilindi!")
    except Exception as e:
        logging.error(f"Xato: {e}")

@dp.message_handler(chat_id=GROUP_ID)
async def cleaner(message: types.Message):
    if not message.text: return
    txt = message.text.lower()
    if message.from_user.username in ["yusufxonpro1", "madiways"]: return
    if any(word in txt for word in BAD_WORDS) or ("http" in txt or "t.me/" in txt):
        try: await message.delete()
        except: pass

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
