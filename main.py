import asyncio
from datetime import datetime
from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- KONFIGURATSIYA ---
API_ID = 35916395
API_HASH = "0a59d023a618c1045b576a5bc0697200"
BOT_TOKEN = "8724439262:AAFGNuQQ4IxdqitlcCEtkHLsvyFwSPg_b1c"
SESSION_STRING = "AgIkCmsAXSW0flyihTLmu1-JWlCeesmW4M_qmRqzcSdTcV28DOqkhkGGbo37stcz44etYaFtrnPjZi-YzJ7PNEh75QfH4spOkTgC_ThKf3FLgXgwKakN-eADRxBRPWj5RAjSSmZA_Vm4YjZhqPpanJzQlh4AQEHGQflPWI0hfa0_7dX-lce6X3aQTsgu-Va5k3_tauo3T5kgZtLyMxElo2sxHeuvZIy_mwvIYpyBfSfNgOvC-JNuzv0SEkAuL8ln3usEF_6j4YFu8ObtBmzOwgS1h6evvsnlEbiIQff-UY7rc6PMwz4xlOvUL6O68XaN90VMZxmkZoGm8D2FlsbxBpJhqNOlWQAAAAHMYynbAA"

TARGET_CHANNEL = "@MADIWAYy"
MY_GROUP_ID = -1002441995574
BOT_USERNAME = "madiway_bot" # Botining userneymini yoz

# Mavzular xaritasi (Topic ID'larni tekshirib ol)
TOPIC_MAP = {
    "europa": 2, "evropa": 2, "rossiya": 4, "russia": 4, "россия": 4, "рф": 4,
    "qirg": 6, "kyrgyzstan": 6, "kazak": 8, "qozog": 8, "казахстан": 8,
    "eron": 10, "iran": 10, "tojik": 12, "tajikistan": 12,
    "germaniya": 14, "germany": 14, "belarus": 16, "gruziya": 18, "ukraina": 20
}

KEYWORDS = ["yuk", "fura", "gruz", "рейс", "груз", "фура", "kerak", "cargo"]

bot = Client("madiway_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("madiway_user", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

@user.on_message(filters.group & filters.text)
async def collector_handler(client, message):
    if message.chat.id == MY_GROUP_ID:
        return

    msg_text = message.text.lower()
    if any(word in msg_text for word in KEYWORDS):
        thread_id = 1 # Topilmasa 'General'ga tushadi
        route_name = "UMUMIY"
        
        for key, t_id in TOPIC_MAP.items():
            if key in msg_text:
                thread_id = t_id
                route_name = key.upper()
                break

        # Sana va vaqt
        now = datetime.now().strftime("%d-%m-%Y | %H:%M")
        contact = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.from_user.id}"
        
        # Reklama va Linklar qo'shilgan matn
        final_msg = (
            f"🏔 <b>MadiWay | Auto-Dispatcher</b> 🚀\n"
            f"━━━━━━━━━━━━━━\n"
            f"📍 <b>Yo'nalish:</b> #{route_name}\n"
            f"📦 <b>E'lon:</b>\n<i>{message.text}</i>\n\n"
            f"👤 <b>Aloqa:</b> {contact}\n"
            f"📅 <b>Sana:</b> {now}\n"
            f"━━━━━━━━━━━━━━\n"
            f"📢 Kanal: {TARGET_CHANNEL}\n"
            f"🤖 Bot: @{BOT_USERNAME}"
        )

        # Tugmalar
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📞 Nomerni ko'rish", url=f"https://t.me/{BOT_USERNAME}?start=get_number"),
                InlineKeyboardButton("📱 Programma", url=f"https://t.me/{BOT_USERNAME}?start=app")
            ]
        ])

        try:
            # 1. Kanalga yuborish
            await user.send_message(TARGET_CHANNEL, final_msg, reply_markup=keyboard)
            
            # 2. Guruhdagi maxsus mavzuga (Topic) yuborish
            # reply_to_message_id bu yerda Topic ID vazifasini bajaradi
            await user.send_message(
                chat_id=MY_GROUP_ID, 
                text=final_msg, 
                reply_to_message_id=thread_id, 
                reply_markup=keyboard
            )
            
            await asyncio.sleep(2)
        except Exception as e:
            print(f"⚠️ Xato yuz berdi: {e}")

async def start_all():
    print("🚀 MadiWay yangilangan tizimi (Topic + Buttons) ishga tushdi...")
    await bot.start()
    await user.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(start_all())
