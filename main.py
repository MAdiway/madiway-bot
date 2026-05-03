import asyncio
import json
from aiogram import Bot, Dispatcher, types, F
from datetime import datetime

TOKEN = "BOT_TOKENI"
CHANNEL_ID = -100123456789 # Kanalingiz yoki guruhingiz ID si

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.content_type == types.ContentType.WEB_APP_DATA)
async def handle_webapp_data(message: types.Message):
    data = json.loads(message.web_app_data.data)
    
    if data['action'] == "auto_yuk":
        topic_id = data['topic_id']
        repeat = int(data['repeat'])
        text = data['text']
        
        # Avto-yuborish funksiyasi
        async def sender():
            for i in range(repeat):
                await bot.send_message(
                    chat_id=CHANNEL_ID,
                    message_thread_id=topic_id,
                    text=f"🚛 **YANGI YUK (MadiWay Auto)**\n\n📍 Yo'nalish: {data['topic_name']}\n📝 Ma'lumot: {text.capitalize()}\n📞 Tel: {message.from_user.id if message.from_user else 'Mavjud emas'}",
                    parse_mode="Markdown"
                )
                if i < repeat - 1:
                    await asyncio.sleep(3600) # Har 1 soatda qayta yuboradi

        if data['now']:
            asyncio.create_task(sender())
            await message.answer(f"✅ Yuk hozir va jami {repeat} marta yuboriladi.")
        else:
            await message.answer(f"🕒 Yukingiz soat {data['time']} da yuboriladigan qilib sozlangan.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
