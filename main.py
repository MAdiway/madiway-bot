import asyncio
import json
from aiogram import Bot, Dispatcher, types, F

# O'zingizning ma'lumotlaringizni qo'ying
TOKEN = "7299092416:AAFTYm1L_5y7X-m2yU6nK-35wYFjK5W5yA8"
GROUP_ID = -1002444342416  # Guruhingiz ID sini aniq tekshiring (-100 bilan boshlanishi shart)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.content_type == types.ContentType.WEB_APP_DATA)
async def web_app_handler(message: types.Message):
    try:
        # Ilovadan kelgan ma'lumotni o'qiymiz
        res = json.loads(message.web_app_data.data)
        
        topic_id = res.get('t_id')
        msg_body = (
            f"🚛 **YANGI YUK BILDIRNOMASI**\n\n"
            f"👤 Mijoz: {res['user']}\n"
            f"📞 Tel: {res['phone']}\n"
            f"📦 Yuk: {res['text']}\n"
            f"⏰ Vaqt: Hozir"
        )

        # TOPIKGA YUBORISH (message_thread_id parametrit muhim)
        await bot.send_message(
            chat_id=GROUP_ID,
            message_thread_id=topic_id,
            text=msg_body,
            parse_mode="Markdown"
        )
        
        await message.answer("✅ Muvaffaqiyatli yuborildi!")
        
    except Exception as e:
        # Agar xato bo'lsa, foydalanuvchiga xabar beradi
        await message.answer(f"❌ Xatolik: {str(e)}\nBot guruhda admin ekanligini tekshiring!")

async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
