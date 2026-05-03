import logging
import json
import datetime
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# --- SOZLAMALAR ---
TOKEN = "8724439262:AAFGNuQQ4IxdqitlcCEtkHLsvyFwSPg_b1c"
GROUP_ID = -1002441995574  # MADIWAY_Gr guruhining ID si
CHANNEL_ID = "@MADIWAYy"
ADMIN_TOPIC = 1  # Guruhni tozalash va admin xabarlari uchun topic

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Anti-Spam lug'ati: {user_id: oxirgi_yuborilgan_vaqt}
last_post_time = {}

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="🚛 MadiWay Ilovasi", web_app=WebAppInfo(url="https://madiway.github.io/madiway-bot/"))
    )
    start_text = "<b>🏔 MadiWay Logistics</b>\n\nXush kelibsiz! Pastdagi tugma orqali yuk e'lonini yuboring."
    await bot.send_message(message.chat.id, start_text, reply_markup=kb, parse_mode="HTML")

@dp.message_handler(content_types=['web_app_data'])
async def web_app_data_handler(message: types.Message):
    user_id = message.from_user.id
    now_time = datetime.datetime.now()

    # 15 soniyalik cheklovni tekshirish
    if user_id in last_post_time:
        diff = (now_time - last_post_time[user_id]).total_seconds()
        if diff < 15:
            await message.answer(f"⚠️ Iltimos, {int(15 - diff)} soniya kuting. Yuklarni har 15 soniyada yuborish mumkin.")
            return

    try:
        data = json.loads(message.web_app_data.data)
        
        # 1. FACE ID LOGIN XABARI (Admin topicga boradi)
        if data.get("type") == "auth":
            auth_text = f"👤 <b>YANGI LOGIN:</b> {data.get('u_name')}\n📞 {data.get('u_phone')}"
            await bot.send_message(GROUP_ID, auth_text, message_thread_id=ADMIN_TOPIC, parse_mode="HTML")
            return

        # 2. YUK E'LONI MATNI
        text = (
            f"🚛 <b>YANGI YUK</b>\n"
            f"📍 Yo'nalish: #{data.get('t_name')}\n"
            f"📦 Yuk: {data.get('desc')}\n"
            f"⏰ Vaqt: {data.get('time')}\n"
            f"━━━━━━━━━━━━━━\n"
            f"👤 Kimdan: {data.get('u_name')}\n"
            f"📞 Tel: {data.get('u_phone')}"
        )

        # Kanalga yuborish
        await bot.send_message(CHANNEL_ID, text, parse_mode="HTML")

        # Guruhdagi tegishli Topicga yuborish (agar faqat kanal tanlanmagan bo'lsa)
        if not data.get("only_channel"):
            topic_id = data.get('t_id')
            await bot.send_message(GROUP_ID, text, message_thread_id=topic_id, parse_mode="HTML")

        # Vaqtni yangilash
        last_post_time[user_id] = now_time

    except Exception as e:
        logging.error(f"Xato: {e}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
