import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# --- SOZLAMALAR ---
# Token va IDlarni sening kodingdan oldim
BOT_TOKEN = "8724439262:AAFGNuQQ4IxdqitlcCEtkHLsvyFwSPg_b1c"
CHANNEL_ID = "@MADIWAYy"
GROUP_ID = "-1002441995574"

# Railway manzilingni shu yerga qo'y:
WEB_APP_URL = "https://madiway-bot-production.up.railway.app/index.html" 

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# --- KLAVIATURALAR ---
def get_main_inline_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("🚚 Yuk Yuborish (Dasturni ochish)", web_app=WebAppInfo(url=WEB_APP_URL)),
        InlineKeyboardButton("📞 Nomerni ko'rish", callback_data="get_number_now"),
        InlineKeyboardButton("📢 Kanalimiz", url="https://t.me/MADIWAYy"),
        InlineKeyboardButton("👥 Gruppa: Pullik lic @madiways", url="https://t.me/madiways")
    )
    return keyboard

def get_contact_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("📱 Kontaktingizni yuboring", request_contact=True))
    return keyboard

# --- START BUYRUG'I ---
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    welcome_text = (
        "🏔 <b>MadiWay | Global Logistics & Dispatch</b> 🚀\n\n"
        "Xalqaro yuk tashish va professional dispetcherlik xizmatlari tarmog'iga xush kelibsiz! "
        "Biz to'rtta davlatni yagona xavfsiz marshrut bilan bog'laymiz:\n\n"
        "🌍 <b>Bizning yo'nalishlar:</b>\n"
        "📍 O'zbekiston 🇺🇿, Qozog'iston 🇰🇿, Rossiya 🇷🇺, Ozarbayjon 🇦🇿\n\n"
        "🛡 <b>Nega aynan MadiWay?</b>\n"
        "✅ Ishonchlilik, Tezkorlik va 24/7 Professional Dispetcherlik.\n\n"
        "🚛 <b>MadiWay — Sizning yukingiz, bizning mas'uliyatimiz!</b>\n\n"
        "📥 Bog'lanish uchun: @madiways\n"
        "🔗 Link: T.me/MADIWAYy\n"
        "👥 Gruppa: Pullik lic @madiways"
    )
    
    try:
        with open("madiway_banner.png", "rb") as photo:
            await bot.send_photo(message.chat.id, photo, caption=welcome_text, reply_markup=get_main_inline_keyboard())
    except:
        await message.answer(welcome_text, reply_markup=get_main_inline_keyboard())

# --- NOMERNI KO'RISH BOSILGANDA ---
@dp.callback_query_handler(text="get_number_now")
async def ask_number(call: types.CallbackQuery):
    await call.message.answer("Iltimos, nomeringizni yuborish uchun pastdagi tugmani bosing 👇", reply_markup=get_contact_keyboard())
    await call.answer()

# --- NOMER KELGANDA ---
@dp.message_handler(content_types=['contact'])
async def handle_contact(message: types.Message):
    phone = message.contact.phone_number
    await message.answer(f"✅ Rahmat! Sizning raqamingiz qabul qilindi: {phone}", reply_markup=types.ReplyKeyboardRemove())
    
    # Nomerni guruhga (Admin topiciga) yuborish
    admin_text = f"👤 Yangi foydalanuvchi: {message.from_user.full_name}\n📞 Nomer: {phone}"
    await bot.send_message(GROUP_ID, admin_text, message_thread_id=1)

# --- BOTNI ISHGA TUSHIRISH ---
if __name__ == "__main__":
    print("✅ MadiWay Bot barcha xatolarsiz ishga tushdi!")
    executor.start_polling(dp, skip_updates=True)
