import logging
import asyncio
import re
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode

# --- SOZLAMALAR ---
BOT_TOKEN = "8724439262:AAFGNuQQ4IxdqitlcCEtkHLsvyFwSPg_b1c"
GROUP_ID = -1002441995574  # Guruh ID
ADMIN_IDS = [123456789, 987654321]  # O'zingning va boshqa adminlarning IDlarini yoz
BAD_WORDS = ["so'kinish1", "so'kinish2", "reklama", "http", "t.me"] # Taqiqlangan so'zlar

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 1. Start bosilganda professional xabar
@dp.message(F.text == "/start")
async def start_handler(message: types.Message):
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
        "🔗 Kanal: <a href='https://t.me/MADIWAYy'>T.me/MADIWAYy</a>\n"
        "👥 Gruppa: Pullik lic @madiways"
    )
    
    # Admin bo'lsa qo'shimcha tugmalar
    if message.from_user.id in ADMIN_IDS:
        kb = [
            [types.KeyboardButton(text="📊 Statistika"), types.KeyboardButton(text="📢 Reklama yuborish")],
            [types.KeyboardButton(text="🚫 Userni bloklash"), types.KeyboardButton(text="✅ Userni ochish")],
            [types.KeyboardButton(text="⚙️ Sozlamalar"), types.KeyboardButton(text="🧹 Guruhni tozalash")],
            [types.KeyboardButton(text="🚚 Yuk yuborish (Web App)", web_app=types.WebAppInfo(url="SENING_URL"))]
        ]
        reply_markup = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    else:
        kb = [[types.KeyboardButton(text="🚚 Tizimga kirish", web_app=types.WebAppInfo(url="SENING_URL"))]]
        reply_markup = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await message.answer(welcome_text, parse_mode=ParseMode.HTML, reply_markup=reply_markup, disable_web_page_preview=True)

# 2. Topic 1 ni (Admin topic) tozalash mantiqi
@dp.message(F.chat.id == GROUP_ID, F.message_thread_id == 1)
async def clean_admin_topic(message: types.Message):
    # Agar xabar adminlardan bo'lmasa va so'kinish yoki reklama bo'lsa
    if message.from_user.id not in ADMIN_IDS:
        content = message.text or message.caption or ""
        # So'kinish yoki linklarni tekshirish
        for word in BAD_WORDS:
            if word.lower() in content.lower():
                await message.delete()
                return

# 3. Har qanday xabarni guruhda nazorat qilish (so'kinishlar uchun)
@dp.message(F.chat.id == GROUP_ID)
async def global_cleaner(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        # Bu yerda ham so'kinishlarni tekshirib o'chirishing mumkin
        pass

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
