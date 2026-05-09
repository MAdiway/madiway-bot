import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# --- SOZLAMALAR ---
BOT_TOKEN = "8724439262:AAFGNuQQ4IxdqitlcCEtkHLsvyFwSPg_b1c"
BOT_USERNAME = "MADIWAYy_Bot"
# Railway manzilingni bu yerga qo'y:
WEB_APP_URL = "https://madiway-bot-production.up.railway.app/index.html" 

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# --- INLINE TUGMALAR (Asosiy xabar ostida) ---
def get_main_inline_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("🚚 Yuk Yuborish (Dasturni ochish)", web_app=WebAppInfo(url=WEB_APP_URL)),
        InlineKeyboardButton("📞 Nomerni yuborish (Tasdiqlash)", callback_data="get_number_now"),
        InlineKeyboardButton("📢 Kanalimiz", url="https://t.me/MADIWAYy"),
        InlineKeyboardButton("👥 Gruppa: Pullik lic @madiways", url="https://t.me/Madiways")
    )
    return keyboard

# --- REPLY TUGMA (Nomer olish uchun) ---
def get_contact_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton("📱 Kontaktingizni yuboring", request_contact=True))
    return keyboard

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    welcome_text = (
        "🏔 MadiWay | Global Logistics & Dispatch 🚀\n\n"
        "Xalqaro yuk tashish va professional dispetcherlik xizmatlari tarmog'iga xush kelibsiz! "
        "Biz to'rtta davlatni yagona xavfsiz marshrut bilan bog'laymiz:\n\n"
        "🌍 **Bizning yo'nalishlar:**\n"
        "📍 O'zbekiston 🇺🇿\n"
        "📍 Qozog'iston 🇰🇿\n"
        "📍 Rossiya 🇷🇺\n"
        "📍 Ozarbayjon 🇦🇿\n\n"
        "🛡 **Nega aynan MadiWay?**\n"
        "✅ Ishonchlilik: Yukingiz manzili va vaqti bizning nazoratimizda.\n"
        "✅ Tezkorlik: Eng qulay va xavfsiz yo'llarni taqdim etamiz.\n"
        "✅ Professional Dispetcherlik: 24/7 aloqa va harakat nazorati.\n\n"
        "🚛 **MadiWay — Sizning yukingiz, bizning mas'uliyatimiz!**\n\n"
        "📥 Bog'lanish uchun: [@Madiways]\n"
link:    T.me/MADIWAYy
Bot @MADIWAYy_bot
Gruppa:Pullik  lic @madiways
    )
    
    try:
        with open("madiway_banner.png", "rb") as photo:
            await bot.send_photo(message.chat.id, photo, caption=welcome_text, reply_markup=get_main_inline_keyboard())
    except:
        await message.answer(welcome_text, reply_markup=get_main_inline_keyboard())

# --- NOMERNI KO'RISH BOSILGANDA ---
@dp.callback_query_handler(text="get_number_now")
async def ask_number(call: types.CallbackQuery):
    await call.message.answer("Iltimos, pastdagi tugmani bosib telefon raqamingizni yuboring 👇", reply_markup=get_contact_keyboard())
    await call.answer()

# --- NOMER KELGANDA ---
@dp.message_handler(content_types=['contact'])
async def handle_contact(message: types.Message):
    phone = message.contact.phone_number
    await message.answer(f"✅ Rahmat! Sizning raqamingiz qabul qilindi: {phone}\nEndi yuk yuborish bo'limidan foydalanishingiz mumkin.", reply_markup=types.ReplyKeyboardRemove())
    # Bu yerda nomerni o'zingga yoki guruhga yuborib qo'ysang ham bo'ladi
    admin_text = f"👤 Yangi foydalanuvchi: {message.from_user.full_name}\n📞 Nomer: {phone}"
    await bot.send_message("-1002441995574", admin_text, message_thread_id=1)

if __name__ == "__main__":
    print("✅ MadiWay Bot barcha tugmalar bilan ishga tushdi!")
    executor.start_polling(dp, skip_updates=True)
