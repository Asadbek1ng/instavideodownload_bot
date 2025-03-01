import asyncio
import yt_dlp
import pinterest_downloader as pd
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.filters import Command

TOKEN = "7566726307:AAFlaBenPmTZn_Xs4uchyWEO9l0Z4gtcnGs"

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def download_video(url):
    if "pinterest.com" in url:
        try:
            pin = pd.Pin(url)  # Pinterest yuklash
            filename = "pinterest_video.mp4"
            pin.video().download(filename=filename)
            return filename
        except Exception as e:
            return f"❌ Pinterest yuklab olishda xatolik: {e}"
    else:
        options = {
            'format': 'best',
            'outtmpl': 'video.%(ext)s',
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            return filename

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Salom! Menga TikTok, Instagram, YouTube yoki Pinterest linkini yuboring!")

@dp.message()
async def handle_message(message: types.Message):
    url = message.text
    if any(site in url for site in ["tiktok.com", "youtube.com", "instagram.com", "pinterest.com"]):
        await message.answer("📥 Videoni yuklab olmoqdaman, kuting...")
        filename = await download_video(url)

        if filename.startswith("❌"):
            await message.answer(filename)  # Xatolik bo‘lsa, xabar yuboriladi
        else:
            try:
                video = FSInputFile(filename)
                await message.answer_video(video)
            except Exception as e:
                await message.answer(f"❌ Xatolik yuz berdi: {e}")
    else:
        await message.answer("❌ Iltimos, to‘g‘ri link yuboring!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
