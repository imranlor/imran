from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import token 
import os, time, logging, requests, random

bot = Bot(token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f"Привет {message.from_user.full_name}")

@dp.message_handler()
async def download_send_video(message:types.Message):
    await message.answer("Скачиваю видео...")
    get_id_video = message.text.split('?')
    current_id = get_id_video[0].split('/')[5]
    video_api = requests.get(f'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={current_id}').json()
    video_url = video_api.get('aweme_list')[0].get('video').get('play_addr').get('url_list')[0]
    print(video_url)
    if video_url:
        title_video = video_api.get('aweme_list')[0].get('desc')
        if title_video != ' ':
            title_video = random.randint(1111, 22222)
        try:
            with open(f'video/{title_video}.mp4', 'wb') as video_file:
                video_file.write(requests.get(video_url).content)
            await message.answer("Видео успешно скачан, отправляю...")
        except Exception as error:
            print(f"Error: {error}")
        try:
            with open(f'video/{title_video}.mp4', 'rb') as send_file:
                await message.answer_video(send_file)
        except Exception as error:
            await message.answer(f"Ошибка: {error}")

executor.start_polling(dp, skip_updates=True)