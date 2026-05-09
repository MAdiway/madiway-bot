import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters

# --- SOZLAMALAR ---
API_ID = 35916395
API_HASH = "0a59d023a618c1045b576a5bc0697200"
BOT_TOKEN = "8724439262:AAFGNuQQ4IxdqitlcCEtkHLsvyFwSPg_b1c"
SESSION_STRING = "AgIkCmsAXSW0flyihTLmu1-JWlCeesmW4M_qmRqzcSdTcV28DOqkhkGGbo37stcz44etYaFtrnPjZi-YzJ7PNEh75QfH4spOkTgC_ThKf3FLgXgwKakN-eADRxBRPWj5RAjSSmZA_Vm4YjZhqPpanJzQlh4AQEHGQflPWI0hfa0_7dX-lce6X3aQTsgu-Va5k3_tauo3T5kgZtLyMxElo2sxHeuvZIy_mwvIYpyBfSfNgOvC-JNuzv0SEkAuL8ln3usEF_6j4YFu8ObtBmzOwgS1h6evvsnlEbiIQff-UY7rc6PMwz4xlOvUL6O68XaN90VMZxmkZoGm8D2FlsbxBpJhqNOlWQAAAAHMYynbAA"

# MUHIM: Har doim qo'shtirnoq ichida yozilishi shart!
TARGET_CHANNEL = "@MADIWAYy"
MY_GROUP_ID = -1002441995574
BOT_USERNAME = "MADIWAYy_Bot"

TOPIC_MAP = {
    "europa": 2, "evropa": 2, "rossiya": 4, "russia": 4, "qirg": 6,
    "kazak": 8, "eron": 10, "tojik": 12, "germaniya": 14,
    "belarus": 16, "gruziya": 18, "ukraina": 20
}
KEYWORDS = ["yuk", "fura", "gruz", "рейс", "груз", "фура", "kerak"]

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
userbot = Client("madiway_user", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("📞 Nomerni ko'rish", url=f"https://t.me/{BOT_USERNAME}?start=get_number"),
        InlineKeyboardButton("📱 Programma", url=f"https://t.me/{BOT_USERNAME}?start=app"),
        InlineKeyboardButton("📢 Kanalimiz", url="https://t.me/MADIWAYy")
    )
    return keyboard

# --- START BUYRUG'I ---
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    welcome_text = (
        "🏔 <b>MadiWay | Global Logistics & Dispatch</b> 🚀\n\n"
        "Xalqaro yuk tashish va professional dispetcherlik xizmatlari tarmog'iga xush kelibsiz!\n\n"
        "🌍 <b>Bizning yo'nalishlar:</b>\n"
        "📍 O'zbekiston 🇺🇿, Qozog'iston 🇰🇿, Rossiya 🇷🇺, Ozarbayjon 🇦🇿\n\n"
        "🛡 <b>Nega MadiWay?</b>\n"
        "✅ Ishonchlilik, Tezkorlik, 24/7 Professional Dispetcherlik.\n\n"
        "🚛 <b>MadiWay — Sizning yukingiz, bizning mas'uliyatimiz!</b>\n\n"
        "📥 Bog'lanish uchun: @Madiways\n"
        "🔗 Link: T.me/MADIWAYy\n"
        "👥 Gruppa: Pullik lic @madiways"
    )
    try:
        # Fayl GitHub-da root papkada bo'lishi kerak
        with open("madiway_banner.png", "rb") as photo:
            await bot.send_photo(message.chat.id, photo, caption=welcome_text, reply_markup=get_main_keyboard())
    except:
        await message.answer(welcome_text, reply_markup=get_main_keyboard())

# --- USERBOT LOGIKASI ---
@userbot.on_message(filters.group & filters.text)
async def handle_new_post(client, message):
    if message.chat.id == MY_GROUP_ID:
        return
    text_lower = message.text.lower()
    if any(word in text_lower for word in KEYWORDS):
        topic_id = 1
        route = "UMUMIY"
        for key, t_id in TOPIC_MAP.items():
            if key in text_lower:
                topic_id = t_id
                route = key.upper()
                break
        
        caption = (
            f"🏔 <b>MadiWay | Auto-Dispatcher</b>\n"
            f"📍 Yo'nalish: #{route}\n\n"
            f"{message.text}\n\n"
            f"👤 Aloqa: @{message.from_user.username if message.from_user.username else 'id_'+str(message.from_user.id)}\n"
            f"📅 Sana: {datetime.now().strftime('%d-%m-%Y')}\n"
            f"━━━━━━━━━━━━━━\n"
            f"📢 Kanal: {TARGET_CHANNEL}"
        )
        try:
            # 73-QATOR: ENDI BU YERDA LINK EMAS, O'ZGARUVCHI TURIBDI
            await bot.send_message(TARGET_CHANNEL, caption, reply_markup=get_main_keyboard())
            await bot.send_message(MY_GROUP_ID, caption, message_thread_id=topic_id, reply_markup=get_main_keyboard())
        except:
            pass

async def on_startup(_):
    await userbot.start()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
