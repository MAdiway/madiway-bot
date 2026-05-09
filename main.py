import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from pyrogram import Client, filters

# --- SOZLAMALAR ---
API_ID = 35916395
API_HASH = "0a59d023a618c1045b576a5bc0697200"
BOT_TOKEN = "8724439262:AAFGNuQQ4IxdqitlcCEtkHLsvyFwSPg_b1c"
SESSION_STRING = "AgIkCmsAXSW0flyihTLmu1-JWlCeesmW4M_qmRqzcSdTcV28DOqkhkGGbo37stcz44etYaFtrnPjZi-YzJ7PNEh75QfH4spOkTgC_ThKf3FLgXgwKakN-eADRxBRPWj5RAjSSmZA_Vm4YjZhqPpanJzQlh4AQEHGQflPWI0hfa0_7dX-lce6X3aQTsgu-Va5k3_tauo3T5kgZtLyMxElo2sxHeuvZIy_mwvIYpyBfSfNgOvC-JNuzv0SEkAuL8ln3usEF_6j4YFu8ObtBmzOwgS1h6evvsnlEbiIQff-UY7rc6PMwz4xlOvUL6O68XaN90VMZxmkZoGm8D2FlsbxBpJhqNOlWQAAAAHMYynbAA"

TARGET_CHANNEL = "@MADIWAYy"
MY_GROUP_ID = -1002441995574  # MADIWAY_Gr ID-si
BOT_USERNAME = "MADIWAYy_Bot"

# --- TOPICLAR XARITASI (ID-lar linklaring bo'yicha) ---
TOPIC_MAP = {
    "europa": 2, "evropa": 2,
    "rossiya": 4, "russia": 4, "россия": 4,
    "qirg": 6, "kyrgyzstan": 6, "киргизия": 6,
    "kazak": 8, "qozog": 8, "казахстан": 8,
    "eron": 10, "iran": 10,
    "tojik": 12, "tajikistan": 12,
    "germaniya": 14, "germany": 14,
    "belarus": 16,
    "gruziya": 18, "georgia": 18,
    "ukraina": 20, "ukraine": 20
}

KEYWORDS = ["yuk", "fura", "gruz", "рейс", "груз", "фура", "kerak", "cargo"]

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
userbot = Client("madiway_user", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# --- KLAVIATURA ---
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("📞 Nomerni ko'rish", url=f"https://t.me/{BOT_USERNAME}?start=get_number"),
        InlineKeyboardButton("📱 Programma", url=f"https://t.me/{BOT_USERNAME}?start=app"),
        InlineKeyboardButton("📢 Kanalimiz", url="https://t.me/MADIWAYy")
    )
    return keyboard

# --- START BUYRUG'I (Banner bilan) ---
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    welcome_text = (
        "🏔 <b>MadiWay | Global Logistics & Dispatch</b> 🚀\n\n"
        "Xalqaro yuk tashish va professional dispetcherlik xizmatlari tarmog'iga xush kelibsiz! "
        "Biz to'rtta davlatni yagona xavfsiz marshrut bilan bog'laymiz:\n\n"
        "🌍 <b>Bizning yo'nalishlar:</b>\n"
        "📍 O'zbekiston 🇺🇿\n"
        "📍 Qozog'iston 🇰🇿\n"
        "📍 Rossiya 🇷🇺\n"
        "📍 Ozarbayjon 🇦🇿\n\n"
        "🛡 <b>Nega aynan MadiWay?</b>\n"
        "✅ Ishonchlilik: Yukingiz manzili va vaqti bizning nazoratimizda.\n"
        "✅ Tezkorlik: Eng qulay va xavfsiz yo'llarni taqdim etamiz.\n"
        "✅ Professional Dispetcherlik: 24/7 aloqa va harakat nazorati.\n\n"
        "🚛 <b>MadiWay — Sizning yukingiz, bizning mas'uliyatimiz!</b>\n\n"
        "📥 Bog'lanish uchun: @Madiways\n"
        "👥 Guruh: Pullik lic @Madiways"
    )
    try:
        banner = InputFile("madiway_banner.png")
        await bot.send_photo(chat_id=message.chat.id, photo=banner, caption=welcome_text, reply_markup=get_main_keyboard())
    except:
        await message.answer(welcome_text, reply_markup=get_main_keyboard())

# --- ASOSIY ISHCHY LOGIKA ---
@userbot.on_message(filters.group & filters.text)
async def handle_new_post(client, message):
    if message.chat.id == MY_GROUP_ID:
        return

    text_lower = message.text.lower()
    if any(word in text_lower for word in KEYWORDS):
        topic_id = 1 # Topilmasa Umumiy (General)
        route = "UMUMIY"
        
        for key, t_id in TOPIC_MAP.items():
            if key in text_lower:
                topic_id = t_id
                route = key.upper()
                break

        now = datetime.now().strftime("%d-%m-%Y | %H:%M")
        username = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.from_user.id}"
        
        caption = (
            f"🏔 <b>MadiWay | Auto-Dispatcher</b> 🚀\n"
            f"━━━━━━━━━━━━━━\n"
            f"📍 <b>Yo'nalish:</b> #{route}\n"
            f"📦 <b>E'lon:</b>\n<i>{message.text}</i>\n\n"
            f"👤 <b>Aloqa:</b> {username}\n"
            f"📅 <b>Sana:</b> {now}\n"
            f"━━━━━━━━━━━━━━\n"
            f"📢 Kanal: {TARGET_CHANNEL}\n"
            f"🤖 Bot: @{BOT_USERNAME}"
        )

        try:
            # Kanalga yuborish
            await bot.send_message(chat_id=TARGET_CHANNEL, text=caption, reply_markup=get_main_keyboard())
            # Guruhdagi aynan sen bergan link bo'yicha Topic-ga yuborish
            await bot.send_message(
                chat_id=MY_GROUP_ID, 
                text=caption, 
                message_thread_id=topic_id, 
                reply_markup=get_main_keyboard()
            )
        except Exception as e:
            print(f"Xato yuz berdi: {e}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(userbot.start())
    executor.start_polling(dp, skip_updates=True)
