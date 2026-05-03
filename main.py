import logging
import json
import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# --- KONFIGURATSIYA ---
TOKEN = "8791239714:AAGeDUktKzciq9ftUp4lZZOzIuyItQXv5wM"
GROUP_ID = -1003996104316
CHANNEL_ID = "@MADIWAYy"
# Rasm manzili (GitHub'dagi manzilingiz)
BANNER_URL = "https://raw.githubusercontent.com/madiway/madiway-bot/main/madiway_banner.png"
WEB_APP_URL = "https://madiway.github.io/madiway-bot/"

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# --- SO'KINISHLAR RO'YXATI ---
BAD_WORDS = [
    "jalab", "qo'toq", "am", "qotoq", "shalpang", "iflos", "yaramas", 
    "dalbayob", "axmoq", "onangni", "otangni", "gey", "pider", 
    "gandon", "lox", "manqurt", "beshaka"
]

# --- START BUYRUG'I (XATOSIZ MATN BILAN) ---
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="🚛 Ilovaga kirish", web_app=WebAppInfo(url=WEB_APP_URL))
    )
    
    # DIQQAT: Markdown xatosi bo'lmasligi uchun matn formatini to'g'riladim
    caption = (
        "🏔 **MadiWay | Global Logistics & Dispatch** 🚀\n\n"
        "Xalqaro yuk tashish va professional dispetcherlik xizmatlari tarmog'iga xush kelibsiz! "
        "Biz to'rtta davlatni yagona xavfsiz marshrut bilan bog'laymiz:\n\n"
        "🌍 **Bizning yo'nalishlar:**\n"
        "📍 O'zbekiston, Qozog'iston, Rossiya, Ozarbayjon\n\n"
        "🛡 **Nega aynan MadiWay?**\n"
        "✅ Ishonchlilik: Yukingiz manzili va vaqti bizning nazoratimizda.\n"
        "✅ Tezkorlik: Eng qulay va xavfsiz yo'llarni taqdim etamiz.\n\n"
        "🚛 **MadiWay — Sizning yukingiz, bizning mas'uliyatimiz!**\n\n"
        "📥 Bog'lanish: @Madiways\n"
        "🔗 Kanal: T.me/MADIWAYy\n"
        "🤖 Bot: @MADIWAYy_bot\n"
        "👥 Gruppa: @MADIWAY_Gr"
    )
    
    try:
        # Rasmni yuborish (Markdown o'rniga HTML ishlatish xavfsizroq)
        await bot.send_photo(
            chat_id=message.chat.id, 
            photo=BANNER_URL, 
            caption=caption, 
            reply_markup=kb, 
            parse_mode="Markdown"
        )
    except Exception as e:
        logging.error(f"Start yuborishda xato: {e}")
        # Agar rasmda yoki formatda xato bo'lsa, oddiy matnni o'zini yuboradi
        await message.answer(caption, reply_markup=kb, parse_mode="Markdown")

# --- WEB APP'DAN KELGAN YUK MA'LUMOTLARI ---
@dp.message_handler(content_types=['web_app_data'])
async def handle_webapp_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        now = datetime.datetime.now().strftime("%d.%m.%Y | %H:%M")
        
        report = (
            f"🚛 **YANGI YUK E'LONI**\n\n"
            f"📍 Yo'nalish: #{data['t_name']}\n"
            f"📦 Tavsif: {data['desc']}\n"
            f"⏰ Vaqt: {data['time']}\n"
            f"👤 Yuboruvchi: {data['u_name']}\n"
            f"📞 Tel: {data['u_phone']}\n"
            f"📅 Sana: {now}"
        )

        kb = InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton("📩 Lichka", url=f"tg://user?id={message.from_user.id}"),
            InlineKeyboardButton("📢 Kanal", url="https://t.me/MADIWAYy"),
            InlineKeyboardButton("👥 Guruh", url="https://t.me/MADIWAY_Gr")
        )

        # Kanalga yuborish
        await bot.send_message(CHANNEL_ID, report, reply_markup=kb, parse_mode="Markdown")
        
        # Guruhga yuborish (Topic bo'lsa t_id ishlaydi)
        try:
            await bot.send_message(GROUP_ID, report, message_thread_id=data['t_id'])
        except:
            await bot.send_message(GROUP_ID, report)
            
    except Exception as e:
        logging.error(f"Ma'lumot yuborishda xato: {e}")

# --- GURUH FILTRI (SO'KINISH VA REKLAMA) ---
@dp.message_handler(chat_id=GROUP_ID)
async def group_filter(message: types.Message):
    if not message.text: return
    text = message.text.lower()
    
    # Adminlarni tekshirmaymiz
    if message.from_user.username in ["yusufxonpro1", "madiways"]:
        return

    # So'kinish yoki reklama bo'lsa
    if any(word in text for word in BAD_WORDS) or ("http" in text or "@" in text):
        try:
            await message.delete()
            if any(word in text for word in BAD_WORDS):
                # 2 kunga ban (48 soat)
                ban_time = datetime.datetime.now() + datetime.timedelta(days=2)
                await bot.restrict_chat_member(GROUP_ID, message.from_user.id, until_date=ban_time)
                await message.answer(f"🚫 {message.from_user.full_name} 2 kunga ban qilindi (Sabab: Odobsizlik).")
        except Exception as e:
            logging.error(f"Filtlashda xato: {e}")

if __name__ == "__main__":
    # skip_updates=True — bot o'chiq turganda yig'ilib qolgan "soatcha" xabarlarni tozalaydi
    executor.start_polling(dp, skip_updates=True)
