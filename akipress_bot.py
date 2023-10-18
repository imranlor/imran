from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from logging import basicConfig, INFO
import os, requests

load_dotenv('.env')

bot = Bot(os.environ.get('token'))
dp = Dispatcher(bot)
basicConfig(level=INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f'Привет {message.from_user.full_name}')

@dp.message_handler(commands='news')
async def get_news(message:types.Message):
    await message.answer("Отправляю новости с сайта...")
    url = 'https://akipress.org'

    response = requests.get(url=url)
    print(response)
    soup = BeautifulSoup(response.text, 'lxml')
    # print(soup)
    all_news = soup.find_all('a', class_='newslink')
    # print(all_news)
    n = 0
    for news in all_news:
        n += 1
        print(f'{n}){news.text}')
        await message.answer(f"{n}) {news.text}")
executor.start_polling(dp, skip_updates=True)