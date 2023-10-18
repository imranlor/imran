from aiogram import Bot, Dispatcher, types, executor
from config import token
from logging import basicConfig, INFO

bot = Bot(token)
dp = Dispatcher(bot)
basicConfig(level=INFO)

start_keyboards = [
    types.KeyboardButton("O нас"),
    types.KeyboardButton("Курсы"),
    types.KeyboardButton("График работы"),
    types.KeyboardButton("Адрес")
]

start_button = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_keyboards)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f"Здравствуйте, {message.from_user.full_name}",reply_markup=start_button)
    print(message)

@dp.message_handler(text="O нас")
async def about(message:types.Message):
    await message.answer("""Образовательный центр Geeks (Гикс) был основан Fullstack-разработчиком Айдаром Бакировым и Android-разработчиком Нургазы Сулаймановым в 2018-ом году в Бишкеке с целью дать возможность каждому человеку, даже без опыта в технологиях, гарантированно освоить IT-профессию.
На сегодняшний день более 1200 студентов в возрасте от 12 до 45 лет изучают здесь самые популярные и востребованные IT-профессии. Филиальная сеть образовательного центра представлена в таких городах, как Бишкек, Ош и Кара-Балта.
""")
    

@dp.message_handler(text="График работы")
async def schedule_time(message:types.Message):
    await message.answer(f"{message.from_user.username} наш график работы\n ПН-СБ 10:00-20:00")

@dp.message_handler(text="Адрес")
async def addres(message:types.Message):
    await message.answer("МЫ находимся по адресу:\nМырзалы Аматова 1Б")
    await message.answer_location(40.51927293359835, 72.80298008693217)

courses_keyboard = [
    types.KeyboardButton("Bakend"),
    types.KeyboardButton("Frontent"),
    types.KeyboardButton("Android"),
    types.KeyboardButton("iOS"),
    types.KeyboardButton("UX/UI"),
    types.KeyboardButton("Главная")
]

courses_button =types.ReplyKeyboardMarkup(resize_keyboard=True).add(*courses_keyboard)

@dp.message_handler(text="Курсы")
async def get_courses(message:types.Message):
    await message.answer("Выберите курсы:", reply_markup=courses_button)

@dp.message_handler(text='Курсы')
async def home(message:types.Message):
    await start(message)


@dp.message_handler(text="Bakend")
async def bakend(message:types.Message):
    await message.answer("""Bakend-Стань Backend-разработчиком с нуля за 5 месяцев и получи доступ к стажировке + помощь в трудоустройстве!""")


@dp.message_handler(text="Frontent")
async def frontend(message:types.Message):
    await message.answer("""Frontend-Стань Frontend-разработчиком с нуля за 5 месяцев и получи доступ к стажировке + помощь в трудоустройстве!""")


@dp.message_handler(text="Android")
async def android(message:types.Message):
    await message.answer("""Android-Стань Android-разработчиком с нуля за 7 месяцев и получи доступ к стажировке + помощь в трудоустройстве!""")


@dp.message_handler(text="iOS")
async def ios(message:types.Message):
    await message.answer("""iOS-Стань iOS-разработчиком с нуля за 7 месяцев и получи доступ к стажировке + помощь в трудоустройстве!""")


@dp.message_handler(text="UX/UI")
async def uxui(message:types.Message):
    await message.answer("""UX/UI-Стань UX/UI-дизайнером с нуля за 3 месяца и получи доступ к стажировке + помощь в трудоустройстве!""")

executor.start_polling(dp)