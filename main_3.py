from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from pytube import YouTube
from dotenv import load_dotenv 
import os
import logging

import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS user (
               user_id INTEGER PRIMARY KEY,
               username TEXT,
               full_name TEXT,
               download_url TEXT

)''')

conn.commit()

load_dotenv('.env')

bot = Bot(os.environ.get("TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name
    download_url = message.from_user.url

    cursor.execute(f"INSERT OR REPLACE INTO user VALUES ('{user_id}', '{username}', '{full_name}', '{download_url}')")
    await message.answer(f"""Здраствуйте, {message.from_user.full_name}
Я вам помогу скачать аудио или же видео с ютуба""")
    conn.commit()
    conn.close()

class DownloadAudio(StatesGroup):
    download = State()

class DownloadVideo(StatesGroup):
    download = State()

def download(url, type):
    yt = YouTube(url)
    if type == "audio":
        yt.streams.filter(only_audio=True).first().download("audio", f"{yt.title}.mp3")
        return f"{yt.title}.mp3"
    elif type == "video":
        yt.streams.filter(progressive=True, file_extension="mp4").first().download("video", f"{yt.title}.mp4")
        return f"{yt.title}.mp4"

@dp.message_handler(text = ["Аудио", "аудио", "Audio", "audio"])
async def audio(message: types.Message):
    await message.answer("Отправьте ссылку на видео и я вам отправлю его в mp3")
    await DownloadAudio.download.set()

@dp.message_handler(text = ["Видео", "видео", "Video", "video"])
async def video(message: types.Message):
    await message.answer("Отправьте ссылку на видео в ютубе и я вам его отправлю")
    await DownloadVideo.download.set()

def record_download(user_id, download_url):
    cursor.execute(f"INSERT INTO user VALUES ('{download_url}', '{user_id}')")
    conn.commit()


@dp.message_handler(state=DownloadAudio.download)
async def download_audio(message: types.Message, state : FSMContext):
    try:
        title = download(message.text, "audio")
        audio = open(f"audio/{title}", "rb")
        await message.answer("Скачиваем файл ожидайте...")
        try:
            await message.answer("Все скачалось вот держи")
            await bot.send_audio(message.chat.id, audio)
            user_id = message.from_user.id
            download_url = message.text
            record_download(user_id, "audio", download_url)
        except:
            await message.answer("Произошла ошибка, попробуйте позже")
        await state.finish()
    except:
        await message.answer("Неверная ссылка на видео")
        await state.finish()

@dp.message_handler(state=DownloadVideo.download)
async def download_video(message: types.Message, state : FSMContext):
    await message.answer("Скачиваем видео файл ожидайте...")
    try:
        title = download(message.text, "video")
        video = open(f"video/{title}", "rb")
        try:
            await message.answer("Все скачалось вот держи")
            await bot.send_video(message.chat.id, video)
            user_id = message.from_user.id
            download_url = message.text
            record_download(user_id, "video", download_url)
        except:
            await message.answer("Произошла ошибка, попробуйте позже")
        await state.finish()
    except:
        await message.answer("Неверная ссылка на видео")
        await state.finish()

@dp.message_handler()
async def not_found(message: types.Message):
    await message.reply("Я вас не понял")

executor.start_polling(dp)