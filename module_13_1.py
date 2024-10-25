from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio

api = '7851360380:AAHjfBfY-c0WXi2gZ3mFYtE9JlUK23Ln4Gk'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button)
kb.add(button2)

kb2 = InlineKeyboardMarkup(row_width=2)
button3 = InlineKeyboardButton(text='Рассчитать колории', callback_data='colories')
button4 = InlineKeyboardButton(text='Формула рассчёта', callback_data='formulas')
kb2.add(button3)
kb2.add(button4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию: ', reply_markup=kb2)


@dp.callback_query_handler(text='colories')
async def set_age(call):
    await call.message.answer('Ввидите свой возраст')
    await UserState.age.set()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 * вес + 6.25 * рост - 5 * возраст + 5')


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью', reply_markup=kb)


@dp.callback_query_handler(text='colories')
async def set_age(call):
    await call.message.answer('Ввидите свой возраст')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_colories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    age = data['age']
    weight = data['weight']
    growth = data['growth']
    colories = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.answer(f'Ваша норма колорий является {colories}')
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
