import logging
import json
import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# --- KONFIGURATSIYA ---
# Yangi tokeningizni shu yerga yozdim
TOKEN = "8724439262:AAFGNuQQ4IxdqitlcCEtkHLsvyFwSPg_b1c"
GROUP_ID = -1003996104316
CHANNEL_ID = "@MADIWAYy"
BANNER_URL = "https://raw.githubusercontent.com/madiway/madiway-bot/main/madiway_banner.png"
WEB_APP_URL = "https://madiway.github.io/madiway-bot/"

# Loglarni sozlash (Xatolarni ko'rish uchun)
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# --- TAQIQLANGAN SO'ZLAR ---
BAD_WORDS = [
    "jalab", "qo'toq", "am", "qotoq", "iflos", "yaramas", "dalbayob", "axmoq", 
    "gey", "pider", "gandon", "lox", "manqurt", "beshaka"
]

# --- START BUYRUG'I ---
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="🚛 Ilovaga kirish", web_app=WebAppInfo(url=WEB_APP_URL))
    )
    
    caption = (
        "🏔 **MadiWay | Global Logistics & Dispatch** 🚀\n\n"
        "Xalqaro yuk tashish va professional dispetcherlik xizmatlari tarmog'iga xush kelibsiz!\n\n"
        "🌍 **Bizning yo'nalishlar:**\n"
        "📍 O'zbekiston, Qozog'iston, Rossiya, Ozarbayjon\n\n"
        "🚛 **MadiWay — Sizning yukingiz, bizning mas'uliyatimiz!**\n\n"
        "📥 Bog'lanish: @Madiways\n"
        "🔗 Kanal: T.me/MADIWAYy\n"
        "👥 Gruppa: @MADIWAY_Gr"
    )
    
    try:
        await bot.send_photo(message.chat.id, photo=BANNER_URL, caption=caption, reply_markup=kb, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Rasm yuborishda xato: {e}")
        await message.answer(caption, reply_markup=kb, parse_mode="Markdown")

# --- WEB APP MA'LUMOTLARINI QABUL QILISH ---
@dp.message_handler(content_types=['web_app_data'])
async def web_app_data_handler(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        now = datetime.datetime.now().strftime("%d.%m.%Y | %H:%M")
        
        text = (
            f"🚛 **YANGI YUK E'LONI**\n\n"
            f"📍 Yo'nalish: #{data.get('t_name', 'Noma'lum')}\n"
            f"📦 Tavsif: {data.get('desc', '-')}\n"
            f"⏰ Vaqt: {data.get('time', '-')}\n"
            f"👤 Yuboruvchi: {data.get('u_name', 'User')}\n"
            f"📞 Tel: {data.get('u_phone', '-')}\n"
            f"📅 Sana: {now}"
        )

        kb = InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton("📩 Lichka", url=f"tg://user?id={message.from_user.id}"),
            InlineKeyboardButton("📢 Kanal", url="https://t.me/MADIWAYy"),
            InlineKeyboardButton("👥 Guruh", url="https://t.me/MADIWAY_Gr")
        )

        # Kanalga yuborish
        await bot.send_message(CHANNEL_ID, text, reply_markup=kb, parse_mode="Markdown")
        
        # Guruhga yuborish
        try:
            await bot.send_message(GROUP_ID, text, message_thread_id=data.get('t_id'))
        except:
            await bot.send_message(GROUP_ID, text)
            
    except Exception as e:
        logging.error(f"Ma'lumot ishlovida xato: {e}")

# --- GURUH FILTRI ---
@dp.message_handler(chat_id=GROUP_ID)
async def group_filter(message: types.Message):
    if not message.text: return
    txt = message.text.lower()
    
    # Adminlarni tekshirmaymiz
    if message.from_user.username in ["yusufxonpro1", "madiways"]:
        return

    # So'kinish yoki reklama bo'lsa o'chirish
    if any(word in txt for word in BAD_WORDS) or ("http" in txt or "@" in txt):
        try:
            await message.delete()
            if any(word in txt for word in BAD_WORDS):
                ban_until = datetime.datetime.now() + datetime.timedelta(days=2)
                await bot.restrict_chat_member(GROUP_ID, message.from_user.id, until_date=ban_until)
        except Exception as e:
            logging.error(f"O'chirishda xato: {e}")

if __name__ == "__main__":
    # skip_updates=True muhim, bu botni yoqqanda eski "soatcha" xabarlarni o'chirib yuboradi
    executor.start_polling(dp, skip_updates=True)
