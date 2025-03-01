import asyncio
import yt_dlp
import pinterest_downloader as pd
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.filters import Command
import os
import time

TOKEN = "YOUR_BOT_TOKEN"

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def download_video(url, message_id):
    unique_filename = f"video_{message_id}_{int(time.time())}.mp4"  # Har safar yangi nom

    if "pinterest.com" in url:
        try:
            pin = pd.Pin(url)  
            pin.video().download(filename=unique_filename)
            return unique_filename
        except Exception as e:
            return f"❌ Pinterest yuklab olishda xatolik: {e}"
    else:
        options = {
            'format': 'best',
            'outtmpl': unique_filename,  # Fayl nomini o‘zgaruvchan qilish
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            return unique_filename

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Salom! Menga TikTok, Instagram, YouTube yoki Pinterest linkini yuboring!")

@dp.message()
async def handle_message(message: types.Message):
    url = message.text
    if any(site in url for site in ["tiktok.com", "youtube.com", "instagram.com", "pinterest.com"]):
        await message.answer("📥 Videoni yuklab olmoqdaman, kuting...")
        filename = await download_video(url, message.message_id)  # Har bir xabarga alohida fayl nomi

        if filename.startswith("❌"):
            await message.answer(filename)  # Xatolik bo‘lsa, xabar yuboriladi
        else:
            try:
                video = FSInputFile(filename)
                await message.answer_video(video)
                os.remove(filename)  # Yuborilgandan keyin faylni o‘chirish
            except Exception as e:
                await message.answer(f"❌ Xatolik yuz berdi: {e}")
    else:
        await message.answer("❌ Iltimos, to‘g‘ri link yuboring!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
