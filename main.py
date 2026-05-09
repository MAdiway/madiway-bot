import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters

# --- KONFIGURATSIYA ---
API_ID = 35916395
API_HASH = "0a59d023a618c1045b576a5bc0697200"
BOT_TOKEN = "8724439262:AAFGNuQQ4IxdqitlcCEtkHLsvyFwSPg_b1c"
SESSION_STRING = "AgIkCmsAXSW0flyihTLmu1-JWlCeesmW4M_qmRqzcSdTcV28DOqkhkGGbo37stcz44etYaFtrnPjZi-YzJ7PNEh75QfH4spOkTgC_ThKf3FLgXgwKakN-eADRxBRPWj5RAjSSmZA_Vm4YjZhqPpanJzQlh4AQEHGQflPWI0hfa0_7dX-lce6X3aQTsgu-Va5k3_tauo3T5kgZtLyMxElo2sxHeuvZIy_mwvIYpyBfSfNgOvC-JNuzv0SEkAuL8ln3usEF_6j4YFu8ObtBmzOwgS1h6evvsnlEbiIQff-UY7rc6PMwz4xlOvUL6O68XaN90VMZxmkZoGm8D2FlsbxBpJhqNOlWQAAAAHMYynbAA"

TARGET_CHANNEL = "@MADIWAYy"
MY_GROUP_ID = -1002441995574
BOT_USERNAME = "madiway_bot"

# Topic ID xaritasi
TOPIC_MAP = {
    "rossiya": 4, "russia": 4, "россия": 4,
    "qozog": 8, "kazak": 8, "казахстан": 8,
    "europa": 2, "evropa": 2, "germaniya": 14
}

KEYWORDS = ["yuk", "fura", "gruz", "рейс", "груз", "фура", "kerak"]

# Bot va Userbotni sozlash
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
userbot = Client("madiway_user", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# --- FUNKSIYALAR ---

def get_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("📞 Nomerni ko'rish", url=f"https://t.me/{BOT_USERNAME}?start=get_number"),
        InlineKeyboardButton("📱 Programma", url=f"https://t.me/{BOT_USERNAME}?start=app")
    )
    return keyboard

@userbot.on_message(filters.group & filters.text)
async def handle_new_post(client, message):
    if message.chat.id == MY_GROUP_ID:
        return

    text_lower = message.text.lower()
    if any(word in text_lower for word in KEYWORDS):
        # Topicni aniqlash
        topic_id = 1 # General
        route = "UMUMIY"
        for key, t_id in TOPIC_MAP.items():
            if key in text_lower:
                topic_id = t_id
                route = key.upper()
                break

        now = datetime.now().strftime("%d-%m-%Y | %H:%M")
        username = f"@{message.from_user.username}" if message.from_user.username else str(message.from_user.id)
        
        caption = (
            f"🏔 <b>MadiWay | Auto-Dispatcher</b>\n"
            f"📍 Yo'nalish: #{route}\n\n"
            f"📦 <b>E'lon:</b>\n<i>{message.text}</i>\n\n"
            f"👤 Aloqa: {username}\n"
            f"📅 Sana: {now}\n"
            f"━━━━━━━━━━━━━━\n"
            f"📢 Kanal: {https://t.me/MADIWAYy}\n"
            f"🤖 Bot: @{MADIWAYy_Bot}"
        )

        try:
            # 1. Kanalga yuborish
            await bot.send_message(https://t.me/MADIWAYy, caption, reply_markup=get_keyboard())
            
            # 2. Guruhdagi Topicga yuborish
            await bot.send_message(
                MY_GROUP_ID, 
                caption, 
                message_thread_id=topic_id, # aiogramda topicga yuborish
                reply_markup=get_keyboard()
            )
        except Exception as e:
            print(f"Xato: {e}")

# Botni ishga tushirish
async def on_startup(_):
    await userbot.start()
    print("✅ Userbot va Aiogram Bot ishga tushdi!")

if __name__ == "__main__":
    # Pyrogramni aiogram bilan birga ishlatish
    loop = asyncio.get_event_loop()
    loop.create_task(userbot.start())
    executor.start_polling(dp, skip_updates=True)
