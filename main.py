import asyncio
from pyrogram import Client, filters, types
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# --- KONFIGURATSIYA ---
API_ID = 35916395
API_HASH = "0a59d023a618c1045b576a5bc0697200"
BOT_TOKEN = "8724439262:AAFGNuQQ4IxdqitlcCEtkHLsvyFwSPg_b1c"

TARGET_CHANNEL = "@MADIWAYy"
MY_GROUP_ID = -1002441995574
WEB_APP_URL = "https://madiway.uz" 
# Botingdagi rasm linki (agar o'zgarmasa shunday qolsin)
IMAGE_URL = "https://i.ibb.co/vzYm8Yx/madiway-banner.jpg" 

TOPIC_MAP = {
    "europa": 2, "evropa": 2, "rossiya": 4, "russia": 4, "россия": 4,
    "qirg": 6, "kyrgyzstan": 6, "kazak": 8, "qozog": 8, "казахстан": 8,
    "eron": 10, "iran": 10, "tojik": 12, "tajikistan": 12,
    "germaniya": 14, "germany": 14, "belarus": 16, "gruziya": 18, "ukraina": 20
}

KEYWORDS = ["yuk bor", "kerak", "fura", "gruz", "рейс", "груз", "фура", "cargo", "truck"]

bot = Client("madiway_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("madiway_user", api_id=API_ID, api_hash=API_HASH)

# --- 1. BOT: /START (RASM BILAN) ---
@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    text = (
        "🏔 <b>MadiWay | Global Logistics</b> 🚀\n\n"
        "Xalqaro yuk tashish tizimiga xush kelibsiz!\n\n"
        "Pastdagi tugmani bosing va ilova orqali yuk e'lonini yuboring.
        tekin va ishonchli va xavfsiz"
    )
    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("🚚 MadiWay Ilovasi", web_app=WebAppInfo(url=WEB_APP_URL))]],
        resize_keyboard=True
    )
    
    # Rasm bilan yuborish
    try:
        await message.reply_photo(photo=IMAGE_URL, caption=text, reply_markup=keyboard)
    except:
        await message.reply_text(text, reply_markup=keyboard)

# --- 2. USERBOT: YUKLARNI NUSXALASH ---
@user.on_message(filters.group & filters.text)
async def collector_handler(client, message):
    if message.chat.id == MY_GROUP_ID:
        return

    msg_text = message.text.lower()
    if any(word in msg_text for word in KEYWORDS):
        thread_id = 1
        route_name = "ANIQLANMAGAN"
        
        for key, t_id in TOPIC_MAP.items():
            if key in msg_text:
                thread_id = t_id
                route_name = key.upper()
                break

        contact = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.from_user.id}"
        
        final_msg = (
            f"🏔 <b>MadiWay | Auto-Dispatcher</b> 🚀\n\n"
            f"📍 <b>Yo'nalish:</b> #{route_name}\n"
            f"📦 <b>E'lon:</b>\n<i>{message.text}</i>\n\n"
            f"━━━━━━━━━━━━━━\n"
            f"🔗 <b>Manba:</b> {message.chat.title}\n"
            f"👤 <b>Aloqa:</b> {contact}\n\n"
            f"✅ <i>Muvaffaqiyatli jo'natildi!</i>"
        )

        try:
            await user.send_message(TARGET_CHANNEL, final_msg)
            await user.send_message(MY_GROUP_ID, final_msg, reply_to_message_id=thread_id)
        except:
            pass

# --- ISHGA TUSHIRISH ---
async def start_all():
    print("🚀 MadiWay Tizimi Railway uchun tayyor!")
    await bot.start()
    await user.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(start_all())
