import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, types, F

# Loglarni Railway-da ko'rish uchun
logging.basicConfig(level=logging.INFO)

TOKEN = "7299092416:AAFTYm1L_5y7X-m2yU6nK-35wYFjK5W5yA8"
GROUP_ID = -1003996104316
CHANNEL_USER = "@MADIWAYy"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.content_type == types.ContentType.WEB_APP_DATA)
async def handle_webapp_data(message: types.Message):
    try:
        res = json.loads(message.web_app_data.data)
        target = res['target']
        
        msg_text = (
            f"🚛 **YANGI YUK E'LONI**\n\n"
            f"📍 **Yo'nalish:** {res['t_name']}\n"
            f"📦 **Yuk:** {res['desc']}\n"
            f"⏰ **Vaqt:** {res['time']}\n"
            f"👤 **Mijoz:** {res['u_name']}\n"
            f"📞 **Telefon:** {res['u_phone']}\n\n"
            f"🤖 #MadiWay Pro v15"
        )

        if target == 'group':
            # Guruh mavzusiga (Topic)
            await bot.send_message(
                chat_id=GROUP_ID,
                message_thread_id=res['t_id'],
                text=msg_text,
                parse_mode="Markdown"
            )
            await message.answer(f"✅ Yuk muvaffaqiyatli guruhning **{res['t_name']}** bo'limiga yuborildi!")
        else:
            # Kanalga
            await bot.send_message(
                chat_id=CHANNEL_USER,
                text=msg_text,
                parse_mode="Markdown"
            )
            await message.answer("✅ Yuk muvaffaqiyatli **Kanalga** yuborildi!")

    except Exception as e:
        logging.error(f"Xato: {e}")
        await message.answer(f"❌ Xatolik yuz berdi: {str(e)}")

async def main():
    # Bot ishga tushganda eski xabarlarni o'qiymaydi (Conflict oldini olish uchun)
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
