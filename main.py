import asyncio
import json
from aiogram import Bot, Dispatcher, types, F

TOKEN = "7299092416:AAFTYm1L_5y7X-m2yU6nK-35wYFjK5W5yA8"
GROUP_ID = -1003963001370  # Sening guruhing ID-si
CHANNEL_ID = "@MADIWAY_Gr" # Kanal username yoki ID-si (Guruh bilan bir xil bo'lsa ham yuboradi)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.content_type == types.ContentType.WEB_APP_DATA)
async def handle_madiway_data(message: types.Message):
    try:
        res = json.loads(message.web_app_data.data)
        
        # Chiroyli xabar matni
        report = (
            f"🚛 **YANGI YUK BILDIRNOMASI**\n\n"
            f"📍 **Yo'nalish:** {res['t_name']}\n"
            f"👤 **Mijoz:** {res['u_name']}\n"
            f"📞 **Telefon:** {res['u_phone']}\n"
            f"📦 **Yuk:** {res['desc']}\n"
            f"🕒 **Vaqt:** {message.date.strftime('%H:%M')}\n\n"
            f"#MadiWay #YukE'lon"
        )

        # 1. GURUHGA YUBORISH (Aynan o'sha TOPIC-ga)
        await bot.send_message(
            chat_id=GROUP_ID,
            message_thread_id=res['t_id'],
            text=report,
            parse_mode="Markdown"
        )

        # 2. KANALGA YUBORISH (Umumiy lenta uchun)
        # Agar kanal va guruh bitta bo'lsa, bu umumiy (General) qismga tushishi mumkin
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=report,
            parse_mode="Markdown"
        )
        
        await message.answer("✅ Yukingiz guruh va kanalga joylandi!")

    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {str(e)}")

async def main():
    print("MadiWay Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
