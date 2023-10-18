from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests, os, logging
from dotenv import load_dotenv


load_dotenv('.env')

bot = Bot(os.environ.get('token'))
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer("Привет, я бот для конвертации валют")
    await message.answer('Выберите валюту на которую хотите обменять: USD, EURO, RUB, KZT')

@dp.message_handler(commands = 'news')
async def get_news(message:types.Message):
    url = "https://www.nbkr.kg/index.jsp?lang=RUS"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    print(soup)
    quotes = soup.find_all('td', class_='exrate')
    n = 0
    for news in quotes:
        n += 1
        with open('parsing.txt', 'a+', encoding="utf-8") as file:
            file.write(f"{n}) {news.text}\n")
            await message.answer(f"{n}) {news.text}")


@dp.message_handler(text = ['USD', 'RUB', 'EURO', 'KZT'])
async def currency(message:types.Message):
    user_currency = message.text
    await message.answer("Теперь введите сумму для конвертации")
    context = dp.current_state(user=message.from_user.id)
    await context.update_data(user_currency=user_currency)

@dp.message_handler()
async def amount(message:types.Message):
    amount = int(message.text)

    context = dp.current_state(user=message.from_user.id)
    data = await context.get_data()
    user_currency = data.get('user_currency')

    url = "https://www.nbkr.kg/index.jsp?lang=RUS"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    
    convert = soup.find_all("td", {"class": "excurr", "class": "exrate"})   
    usd = float(convert[0].text.replace(',', '.'))
    eur = float(convert[2].text.replace(',', '.'))
    rub = float(convert[4].text.replace(',', '.'))
    kzt = float(convert[6].text.replace(',', '.'))

    if user_currency == "USD":
        result = amount / usd
        await message.answer(f"Результат: {result}")
    elif user_currency == "EURO":
        result = amount / eur
        await message.answer(f"Результат: {result}")
    elif user_currency == "RUB":
        result = amount / rub
        await message.answer(f"Результат: {result}")
    elif user_currency == "KZT":
        result = amount / kzt
        await message.answer(f"Результат: {result}")
    else:
        result = 0.0
        await message.answer(result)
    


executor.start_polling(dp)