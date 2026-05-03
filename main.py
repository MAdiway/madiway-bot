import asyncio
import json
from aiogram import Bot, Dispatcher, types, F

TOKEN = "7299092416:AAFTYm1L_5y7X-m2yU6nK-35wYFjK5W5yA8"
GROUP_ID = -1003996104316  # Sening guruhing
CHANNEL_ID = -1003996104316 # Agar kanal ID boshqa bo'lsa buni ham -100 bilan boshlanadigan ID ga o'zgartir

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.content_type == types.ContentType.WEB_APP_DATA)
async def process_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        target = data['target']
        
        text = (
            f"🚛 **YANGI YUK BILDIRNOMASI**\n\n"
            f"📍 **Yo'nalish:** {data['t_name']}\n"
            f"📦 **Yuk:** {data['desc']}\n"
            f"⏰ **Vaqt:** {data['time']}\n"
            f"👤 **Mijoz:** {data['u_name']}\n"
            f"📞 **Telefon:** {data['u_phone']}\n\n"
            f"🤖 #MadiWay Pro v14"
        )

        if target == 'group':
            # GURUH TOPIKIGA
            await bot.send_message(
                chat_id=GROUP_ID,
                message_thread_id=data['t_id'],
                text=text,
                parse_mode="Markdown"
            )
            await message.answer(f"✅ Yuk muvaffaqiyatli guruhning **{data['t_name']}** topiciga yuklandi!")
        
        else:
            # KANALGA
            # Kanal ID sini o'zingning kanal username yoki ID si bilan almashtirishing mumkin
            await bot.send_message(
                chat_id="@MADIWAYy", 
                text=text,
                parse_mode="Markdown"
            )
            await message.answer("✅ Yuk muvaffaqiyatli **Kanalga** yuklandi!")

    except Exception as e:
        await message.answer(f"❌ Xatolik: {str(e)}\nBot guruh va kanalda admin ekanligini tekshiring!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
