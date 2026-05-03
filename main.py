import asyncio
import json
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart

# --- SOZLAMALAR ---
TOKEN = "BOT_TOKENI_SHU_YERGA"
ADMIN_ID = 5406082447  # Yusufxon sizning ID
# Guruh yoki kanal ID sini (masalan: -100...) yozing
GROUP_ID = -1002444342416 # O'zingizning guruh ID si

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# WebApp ochish uchun tugma
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    kb = [
        [types.InlineKeyboardButton(text="🚛 MadiWay Ilovani ochish", 
                                    web_app=types.WebAppInfo(url="https://SAYTINGIZ_LINKI.com"))]
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer(f"Salom {message.from_user.first_name}!\nMadiWay - Yuklarni avtomatik boshqarish tizimi.", reply_markup=markup)

# WebApp dan ma'lumot kelganda ishlovchi funksiya
@dp.message(F.content_type == types.ContentType.WEB_APP_DATA)
async def handle_webapp_data(message: types.Message):
    try:
        raw_data = message.web_app_data.data
        data = json.loads(raw_data)
        
        if data.get("action") == "auto_yuk":
            topic_id = data.get("topic_id")
            text = data.get("text")
            send_now = data.get("now")
            send_time = data.get("time")
            repeat_count = int(data.get("repeat", 1))

            async def send_to_group():
                for i in range(repeat_count):
                    msg_body = (
                        f"🚛 **YANGI YUK E'LONI**\n\n"
                        f"📝 **Ma'lumot:** {text.capitalize()}\n"
                        f"👤 **Yuboruvchi:** {message.from_user.full_name}\n"
                        f"📞 **Aloqa:** `{message.from_user.id}`\n\n"
                        f"🤖 _MadiWay Smart Bot tomonidan yuborildi_"
                    )
                    
                    # Kerakli topic (mavzu)ga yuborish
                    await bot.send_message(
                        chat_id=GROUP_ID,
                        message_thread_id=topic_id,
                        text=msg_body,
                        parse_mode="Markdown"
                    )
                    
                    # Agar bir necha marta bo'lsa, 1 soat kutish
                    if i < repeat_count - 1:
                        await asyncio.sleep(3600)

            # Vaqtni tekshirish
            if send_now:
                asyncio.create_task(send_to_group())
                await message.answer("✅ Yukingiz hozir guruhga yuborildi!")
            else:
                # Belgilangan vaqtda yuborish logikasi
                now = datetime.now()
                target_time = datetime.strptime(send_time, "%H:%M").replace(
                    year=now.year, month=now.month, day=now.day
                )
                
                delay = (target_time - now).total_seconds()
                if delay < 0: # Agar vaqt o'tib ketgan bo'lsa, ertangi kunga o'tkazish
                    delay += 86400 

                await message.answer(f"🕒 Yukingiz qabul qilindi. Soat {send_time} da avtomatik yuboriladi.")
                
                async def delayed_send():
                    await asyncio.sleep(delay)
                    await send_to_group()
                
                asyncio.create_task(delayed_send())

    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await message.answer("❌ Ma'lumotlarni qayta ishlashda xatolik yuz berdi.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())import asyncio
import json
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart

# --- SOZLAMALAR ---
TOKEN = "BOT_TOKENI_SHU_YERGA"
ADMIN_ID = 5406082447  # Yusufxon sizning ID
# Guruh yoki kanal ID sini (masalan: -100...) yozing
GROUP_ID = -1002444342416 # O'zingizning guruh ID si

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# WebApp ochish uchun tugma
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    kb = [
        [types.InlineKeyboardButton(text="🚛 MadiWay Ilovani ochish", 
                                    web_app=types.WebAppInfo(url="https://SAYTINGIZ_LINKI.com"))]
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer(f"Salom {message.from_user.first_name}!\nMadiWay - Yuklarni avtomatik boshqarish tizimi.", reply_markup=markup)

# WebApp dan ma'lumot kelganda ishlovchi funksiya
@dp.message(F.content_type == types.ContentType.WEB_APP_DATA)
async def handle_webapp_data(message: types.Message):
    try:
        raw_data = message.web_app_data.data
        data = json.loads(raw_data)
        
        if data.get("action") == "auto_yuk":
            topic_id = data.get("topic_id")
            text = data.get("text")
            send_now = data.get("now")
            send_time = data.get("time")
            repeat_count = int(data.get("repeat", 1))

            async def send_to_group():
                for i in range(repeat_count):
                    msg_body = (
                        f"🚛 **YANGI YUK E'LONI**\n\n"
                        f"📝 **Ma'lumot:** {text.capitalize()}\n"
                        f"👤 **Yuboruvchi:** {message.from_user.full_name}\n"
                        f"📞 **Aloqa:** `{message.from_user.id}`\n\n"
                        f"🤖 _MadiWay Smart Bot tomonidan yuborildi_"
                    )
                    
                    # Kerakli topic (mavzu)ga yuborish
                    await bot.send_message(
                        chat_id=GROUP_ID,
                        message_thread_id=topic_id,
                        text=msg_body,
                        parse_mode="Markdown"
                    )
                    
                    # Agar bir necha marta bo'lsa, 1 soat kutish
                    if i < repeat_count - 1:
                        await asyncio.sleep(3600)

            # Vaqtni tekshirish
            if send_now:
                asyncio.create_task(send_to_group())
                await message.answer("✅ Yukingiz hozir guruhga yuborildi!")
            else:
                # Belgilangan vaqtda yuborish logikasi
                now = datetime.now()
                target_time = datetime.strptime(send_time, "%H:%M").replace(
                    year=now.year, month=now.month, day=now.day
                )
                
                delay = (target_time - now).total_seconds()
                if delay < 0: # Agar vaqt o'tib ketgan bo'lsa, ertangi kunga o'tkazish
                    delay += 86400 

                await message.answer(f"🕒 Yukingiz qabul qilindi. Soat {send_time} da avtomatik yuboriladi.")
                
                async def delayed_send():
                    await asyncio.sleep(delay)
                    await send_to_group()
                
                asyncio.create_task(delayed_send())

    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await message.answer("❌ Ma'lumotlarni qayta ishlashda xatolik yuz berdi.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
