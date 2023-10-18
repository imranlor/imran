from aiogram import Bot, Dispatcher, types, executor
from config import token
import random   

bot = Bot(token)
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def start(message:types.Message):
    await message.answer(f"Привет {message.from_user.full_name}!")

@dp.message_handler(text=[1,2,3])
async def select(message:types.Message):
        number = random.randint(1,3)
        user = int(message.text)
        if user ==number:
            await message.answer(f"Вы угадали. Бот выбрал: {number}")
        else:
            await message.reply(f" Вы проиграли. Бот выбрал: {number}")

@dp.message_handler(text="want_to_play_more")
async def want_to_play_more(message:types.Message):
     await message.answer("Да")
     await message.answer("Нет")

executor.start_polling(dp)
