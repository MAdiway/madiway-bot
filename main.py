import logging
import json
import datetime
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# --- KONFIGURATSIYA ---
# Tokenni BotFather'dan olingan eng yangisi bilan tekshiring
TOKEN = "8724439262:AAFGNuQQ4IxdqitlcCEtkHLsvyFwSPg_b1c"
GROUP_ID = -1003996104316
CHANNEL_ID = "@MADIWAYy"
BANNER_URL = "https://raw.githubusercontent.com/madiway/madiway-bot/main/madiway_banner.png"
WEB_APP_URL = "https://madiway.github.io/madiway-bot/" # GitHub Pages manzilingiz

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

BAD_WORDS = ["jalab", "qo'toq", "am", "qotoq", "iflos", "yaramas", "dalbayob", "axmoq", "gandon", "pider"]

# --- START BUYRUG'I ---
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="🚛 MadiWay Ilovasi", web_app=WebAppInfo(url=WEB_APP_URL))
    )
    
    caption = (
        "🏔 **MadiWay | Global Logistics** 🚀\n\n"
        "Xalqaro yuk tashish tizimiga xush kelibsiz!\n\n"
        "Pastdagi tugmani bosing va Face ID orqali tizimga kiring.\n\n"
        "📢 Kanal: T.me/MADIWAYy\n"
        "👥 Guruh: @MADIWAY_Gr"
    )
    
    try:
        await bot.send_photo(message.chat.id, photo=BANNER_URL, caption=caption, reply_markup=kb, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Xato: {e}")
        await message.answer(caption, reply_markup=kb, parse_mode="Markdown")

# --- WEB APP'DAN MA'LUMOT QABUL QILISH ---
@dp.message_handler(content_types=['web_app_data'])
async def web_app_data_handler(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        now = datetime.datetime.now().strftime("%d.%m.%Y | %H:%M")
        
        # Web App'dan kelayotgan t_name, desc, time, u_name, u_phone ni ishlatamiz
        text = (
            f"🚛 **YANGI YUK E'LONI**\n"
            f"━━━━━━━━━━━━━━\n"
            f"📍 **Yo'nalish:** #{data.get('t_name', 'Noma\'lum')}\n"
            f"📦 **Yuk:** {data.get('desc', 'Tavsif yo\'q')}\n"
            f"⏰ **Vaqt:** {data.get('time', 'Hozir')}\n"
            f"━━━━━━━━━━━━━━\n"
            f"👤 **Yuboruvchi:** {data.get('u_name', 'Mijoz')}\n"
            f"📞 **Tel:** {data.get('u_phone', 'Noma\'lum')}\n"
            f"📅 **Sana:** {now}"
        )

        kb = InlineKeyboardMarkup().add(
            InlineKeyboardButton("💬 Bog'lanish", url=f"tg://user?id={message.from_user.id}")
        )

        # Kanalga yuborish
        await bot.send_message(CHANNEL_ID, text, reply_markup=kb, parse_mode="Markdown")
        
        # Guruhga yuborish (Topic ID bo'lsa t_id orqali, bo'lmasa oddiy)
        try:
            await bot.send_message(GROUP_ID, text, message_thread_id=data.get('t_id'), reply_markup=kb, parse_mode="Markdown")
        except:
            await bot.send_message(GROUP_ID, text, reply_markup=kb, parse_mode="Markdown")

        await message.answer("✅ E'loningiz barcha tarmoqlarga yuborildi!")
        
    except Exception as e:
        logging.error(f"Xato: {e}")

# --- GURUHNI TOZALASH ---
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
