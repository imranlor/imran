import os
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Command
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=os.environ.get('token'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

currency_buttons = [
    InlineKeyboardButton('USD', callback_data="usd"),
    InlineKeyboardButton('EUR', callback_data="eur"),
    InlineKeyboardButton('RUB', callback_data="rub"),
    InlineKeyboardButton('KZT', callback_data="kzt"),
]
currency_keyboard = InlineKeyboardMarkup().add(*currency_buttons)

class Money(StatesGroup):
    money = State()

async def get_currency_rate(currency_code):
    url = 'https://www.nbkr.kg/index.jsp?lang=RUS'  # Default URL for USD
    if currency_code == 'eur':
        url = 'URL_для_курса_EUR'
    elif currency_code == 'rub':
        url = 'URL_для_курса_RUB'
    elif currency_code == 'kzt':
        url = 'URL_для_курса_KZT'
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    currencies = soup.find_all('td', class_='exrate')
    return float(currencies[0].text.replace(',', '.'))

async def handle_currency_conversion(message, state, currency_code):
    data = await state.get_data()
    money = data.get('money')

    if money is not None:
        try:
            money = float(money)
            rate = await get_currency_rate(currency_code)
            if rate is not None:
                result = money * rate
                await message.answer(f"Результат: {result} {currency_code.upper()}")
            else:
                await message.answer(f"Не удалось получить курс для {currency_code.upper()}")
        except ValueError:
            await message.answer("Введено некорректное значение денег")
    else:
        await message.answer("Не удалось получить значение денег")

@dp.callback_query_handler(lambda call: call.data in ["usd", "eur", "rub", "kzt"])
async def handle_currency_callback(call: types.CallbackQuery, state: FSMContext):
    currency_code = call.data
    await handle_currency_conversion(call.message, state, currency_code)

@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer("Здравствуйте! Я бот, который обменяет ваши деньги. Введите кол-во денег")
    await Money.money.set()

@dp.message_handler(commands="currency")
async def currency(message: types.Message):
    await message.answer("Теперь выберите валюту для обмена", reply_markup=currency_keyboard)

@dp.message_handler(state=Money.money)
async def money(message: types.Message, state: FSMContext):
    await state.update_data(money=message.text)
    await message.answer("Значение сохранено. Выберите валюту для обмена.", reply_markup=currency_keyboard)
    await Money.next()

executor.start_polling(dp)
