from aiogram import Bot, Dispatcher, types, executor
from config import token
import logging

bot = Bot(token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

start_buttons = [
    types.KeyboardButton('Backend'), 
    types.KeyboardButton('Frontend'),
    types.KeyboardButton('UX/UI'),
    types.KeyboardButton('Android'),
    types.KeyboardButton('iOS')
]

@dp.message_handler(commands='start')
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer(f"Здравствуйте, {message.from_user.full_name}", reply_markup=keyboard)

@dp.message_handler(text="Backend")  
async def backend(message: types.Message):
    await message.answer("""Backend — это внутренняя часть сайта и сервера и т.д
Стоимость 10000 сом в месяц
Обучение: 5 месяц""")

@dp.message_handler(text="Frontend")
async def frontend(message: types.Message):
    await message.answer("""Frontend — это внутренняя часть сайта и сервера и т.д
Стоимость 10000 сом в месяц
Обучение: 5 месяц""")


@dp.message_handler(text="Android")
async def frontend(message: types.Message):
    await message.answer("""Frontend — это внутренняя часть сайта и сервера и т.д
Стоимость 10000 сом в месяц
Обучение: 5 месяц""")


@dp.message_handler(text="iOS")
async def frontend(message: types.Message):
    await message.answer("""Frontend — это внутренняя часть сайта и сервера и т.д
Стоимость 10000 сом в месяц
Обучение: 5 месяц""")

@dp.message_handler(text="UX/UI")
async def frontend(message: types.Message):
    await message.answer("""Frontend — это внутренняя часть сайта и сервера и т.д
Стоимость 10000 сом в месяц
Обучение: 5 месяц""")

executor.start_polling(dp)