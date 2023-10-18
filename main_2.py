from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from pytube import YouTube
from dotenv import load_dotenv
import os
import logging

load_dotenv('.env')

buttnons = [
    KeyboardButton('/start'),
    KeyboardButton('/help'),
    KeyboardButton('/video'),
    KeyboardButton('/audio')
]

buttnon = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*buttnons)

bot = Bot(os.environ.get("TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage)
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

def url_valid(url):
    try:
        YouTube(url).stream.first()
        return True
    except:
        return False
    
@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    await message.answer(f'Здравствуйте {message.from_user.full_name}', reply_markup=buttnon)

class DowloadVideo(StatesGroup):
    dowload = State()

@dp.message_handler(commands=['video'])
async def video(message:types.Message):
    await message.reply(f'Отправте сылку на видео, и я вам скачаю его')
    await DowloadVideo.dowload.set()

@dp.message_handler(state=DowloadVideo.dowload)
async def dowload_video(message:types.Message, state:FSMContext):
    if url_valid(message.text) == True:
        await message .answer("Скачиваем видео")
        yt = YouTube(message.text)
        await message.reply(f'yt.title')
        video = yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first().download('video', f'{yt.title}.mp4')
        try:
            await message.answer("Отправляем видео")
            with open(video, 'rb' ) as down_video:
              await message.answer_video(down_video)
              os.remove(video)

        except:
            await message.answer("Произошла ошибка")
            os.remove(video)

        await state.finish()
    
    else:
        await message.reply("Сылка не децствительна")

class DowloadAudio(StatesGroup):
    dowload = State()

@dp.message_handler(commands='[audio]')
async def audio(message:types.Message):
    await message.reply(f'Отправте сылку на аудио')
    await DowloadVideo.dowload.set()

@dp.message_handler(state =DowloadAudio.dowload)
async def dowload_audio(message:types.Message, state:FSMContext):
    if url_valid(message.text):

        await message.answer("Скачиваем Аудио")
        aud_yt = YouTube(message.text)
        await message.reply(f'{aud_yt.title}')
        audio = aud_yt.streams.filter(only_audio=True).first().download('audio', f'{aud_yt.title}.mp3')

        try:
            await message.answer("скачиваем аудио")
            with open(audio, 'rb') as down_audio:
                await message.answer_audio(down_audio)
                os.remove(audio)
        except:
            await message.answer("произошла ошибка")
            os.remove(audio)

        await state.finish()
    else:
        await message.reply(f'Я вас не понял, ведите /help')

executor.start_polling(dp)