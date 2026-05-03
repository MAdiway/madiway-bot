import logging
import json
import datetime
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# --- ASOSIY MA'LUMOTLAR ---
TOKEN = "8724439262:AAFGNuQQ4IxdqitlcCEtkHLsvyFwSPg_b1c"
GROUP_ID = -1003996104316
CHANNEL_ID = "@MADIWAYy"
BANNER_URL = "https://raw.githubusercontent.com/madiway/madiway-bot/main/madiway_banner.png"
WEB_APP_URL = "https://madiway.github.io/madiway-bot/"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# --- FILTR ---
BAD_WORDS = ["jalab", "qo'toq", "am", "qotoq", "iflos", "yaramas", "dalbayob", "axmoq", "gandon", "pider"]

# --- START BUYRUG'I ---
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="🚛 MadiWay Ilovasi", web_app=WebAppInfo(url=WEB_APP_URL))
    )
    
    caption = (
        "🏔 **MadiWay | Global Logistics** 🚀\n\n"
        "Xush kelibsiz! Face ID orqali tizimga kiring va yuk e'loningizni qoldiring.\n\n"
        "📢 Kanal: T.me/MADIWAYy\n"
        "👥 Guruh: @MADIWAY_Gr"
    )
    
    try:
        await bot.send_photo(message.chat.id, photo=BANNER_URL, caption=caption, reply_markup=kb, parse_mode="Markdown")
    except:
        await message.answer(caption, reply_markup=kb, parse_mode="Markdown")

# --- WEB APP MA'LUMOTI (E'LONLAR) ---
@dp.message_handler(content_types=['web_app_data'])
async def web_app_data_handler(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        
        text = (
            f"🚛 **YANGI YUK E'LONI**\n"
            f"━━━━━━━━━━━━━━\n"
            f"📍 **Yo'nalish:** #{data.get('t_name')}\n"
            f"📦 **Yuk:** {data.get('desc')}\n"
            f"⏰ **Vaqt:** {data.get('time')}\n"
            f"━━━━━━━━━━━━━━\n"
            f"👤 **Yuboruvchi:** {data.get('u_name')}\n"
            f"📞 **Tel:** {data.get('u_phone')}\n"
            f"📅 **Sana:** {datetime.datetime.now().strftime('%d.%m.%Y')}"
        )

        kb = InlineKeyboardMarkup().add(
            InlineKeyboardButton("💬 Bog'lanish", url=f"tg://user?id={message.from_user.id}")
        )

        # Kanal va Guruhga (Topic bo'yicha) yuborish
        await bot.send_message(CHANNEL_ID, text, reply_markup=kb, parse_mode="Markdown")
        try:
            await bot.send_message(GROUP_ID, text, message_thread_id=data.get('t_id'), reply_markup=kb, parse_mode="Markdown")
        except:
            await bot.send_message(GROUP_ID, text, reply_markup=kb, parse_mode="Markdown")

        await message.answer("✅ E'loningiz barcha tarmoqlarga yuborildi!")
    except Exception as e:
        logging.error(f"Xato: {e}")

# --- GURUH MODERATSIYASI ---
@dp.message_handler(chat_id=GROUP_ID)
async def cleaner(message: types.Message):
    if not message.text: return
    txt = message.text.lower()
    
    # Adminlarni o'tkazib yuboramiz
    if message.from_user.username in ["yusufxonpro1", "madiways"]: return

    is_bad = any(word in txt for word in BAD_WORDS)
    is_promo = ("http" in txt) or ("t.me/" in txt) or ("@" in txt and "@madiway" not in txt)

    if is_bad or is_promo:
        try:
            await message.delete()
            warn = await message.answer(f"⚠️ @{message.from_user.username} qoidalarni buzmang!")
            await asyncio.sleep(5)
            await warn.delete()
        except: pass

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
