from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from config import token
import sqlite3, time, logging

bot = Bot(token)

storage = MemoryStorage()  
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

db_users = sqlite3.connect('users.db')
cursor_users = db_users.cursor()
cursor_users.execute("""
    CREATE TABLE IF NOT EXISTS users (
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        username VARCHAR(255),
        id_user INTEGER,
        phone_number INTEGER
    ); 
""")
cursor_users.connection.commit()

db_address = sqlite3.connect('address.db')
cursor = db_address.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS address(
    user_id INT,
    address_longitude INT,
    address_latitude INT
);
""")
cursor.connection.commit()

db_orders = sqlite3.connect('orders.db')
cursor_orders = db_orders.cursor()
cursor_orders.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        title VARCHAR(255),
        address_destination VARCHAR(255),
        date_time_order VARCHAR(255)
    );
""")
cursor_orders.connection.commit()

inline_buttons = [
    InlineKeyboardButton('Отправить номер', callback_data='number'),
    InlineKeyboardButton('Отправить локацию',callback_data='location'),
    InlineKeyboardButton('Заказать еду', callback_data='food')
]
inline_keyboard = InlineKeyboardMarkup().add(*inline_buttons)

num_button = [
    KeyboardButton('Подтвердить номер', request_contact=True)
]
loc_button = [
    KeyboardButton('Подтвердить локацию', request_location=True)
]

orde_button = [
    KeyboardButton('Что хотите выбрать: 1) Пицца, 2) Гамбургер, 3) Хот_дог.')
]

number = ReplyKeyboardMarkup(resize_keyboard=True).add(*num_button)
location = ReplyKeyboardMarkup(resize_keyboard=True).add(*loc_button)
orders = ReplyKeyboardMarkup(resize_keyboard=True).add(*orde_button)

@dp.callback_query_handler(lambda call : call)
async def inline(call):
    if call.data == 'number':
        await get_num(call.message)
    elif call.data == 'location':
        await get_loc(call.message)
    elif call.data == 'food':
        await bot.send_message(call.message.chat.id, 'Закажите все что угодно, достанем')
        await OrderState.food.set()

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f'Здравствуйте, {message.from_user.full_name}')
    await message.answer("В этом боте вы можете оставить свой заказ на пиццу.\n\nНо не забывайте оставить ваш адрес и контактный номер!!!", reply_markup=inline_keyboard)
    cursor_users = db_users.cursor()
    cursor_users.execute("SELECT * FROM users")
    result = cursor_users.fetchall()
    if result == []:
        cursor_users.execute(f"INSERT INTO users VALUES ('{message.from_user.first_name}', '{message.from_user.last_name}', '{message.from_user.username}', '{message.from_user.id}', 'None');")
    db_users.commit()

@dp.message_handler(commands='contact')
async def get_num(message:types.Message):
    await message.answer("Подтвердите свой номер", reply_markup=number)

@dp.message_handler(commands='location')
async def get_loc(message:types.Message):
    await message.answer("Подтвердите свою локацию", reply_markup=location)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def add_number(message:types.Message):
    cursor = db_users.cursor()
    cursor.execute(f"UPDATE users SET phone_number = '{message.contact['phone_number']}' WHERE id_user = {message.from_user.id};")
    db_users.commit()
    await message.answer("Ваш номер успешно добавлен.",reply_markup=inline_keyboard)

@dp.message_handler(content_types=types.ContentType.LOCATION)
async def add_loc(message:types.Message):
    address = f"{message.location.longitude}, {message.location.latitude}"
    cursor = db_address.cursor()
    cursor.execute('SELECT * FROM address')
    res = cursor.fetchall()
    if res == []:
        cursor.execute(f"INSERT INTO address VALUES ('{message.from_user.id}', '{message.location.longitude}', '{message.location.latitude}');")
    db_address.commit()
    await message.answer("Ваш адрес успешно записан", reply_markup=types.ReplyKeyboardRemove())


class OrderState(StatesGroup):
    food = State()
    address = State()

@dp.message_handler(state=OrderState.food)
async def order(message:types.Message, state=FSMContext):
    await state.update_data(food=message.text)
    await message.answer('Отправьте ваш адрес')
    await OrderState.address.set()

@dp.message_handler(state=OrderState.address)
async def address(message:types.Message, state=FSMContext):
    await state.update_data(address=message.text)
    data = await state.get_data()
    cursor = db_orders.cursor()
    cursor.execute(f"INSERT INTO orders VALUES('{data['food']}', '{data['address']}', '{time.ctime()}')")
    db_orders.commit()
    await state.finish()
    await message.answer("Ожидайте, ваш заказ принят")
    
executor.start_polling(dp)