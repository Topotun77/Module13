# Домашнее задание по теме "Машина состояний".
# Цель: получить навык работы с состояниями в телеграм-боте.
#
# Задача "Цепочка вопросов":
# Необходимо сделать цепочку обработки состояний для нахождения нормы калорий для человека.
# Группа состояний:
# Импортируйте классы State и StateGroup из aiogram.dispatcher.filters.state.
# Создайте класс UserState наследованный от StateGroup.
# Внутри этого класса опишите 3 объекта класса State: age, growth, weight (возраст, рост, вес).

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
# import asyncio
import logging

API = 'XXX'
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(
    filename='tg-bot.log', filemode='w', encoding='utf-8',
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    level=logging.INFO)


def decor_log(func, message, txt):
    async def log_writer(*args, **kwargs):
        logging.info(f'Получено сообщение от {message["from"]["first_name"]}: {message["text"]}')
        # logging.info(f'Вся информация: {message}')
        rez = await func(*args, **kwargs)
        logging.info(f'Отправлен ответ: {txt}')
        return rez

    return log_writer


class UserState(StatesGroup):
    gender = State()
    age = State()
    growth = State()
    weight = State()

class UserData():
    DATA = {}


@dp.message_handler(commands=['start'])
async def start(message):
    txt = ('Привет! Я бот помогающий твоему здоровью. Хотите узнать сколько калорий '
           'вам нужно потреблять в день для здорового питания? Отправьте слово "Калории".')
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt)


@dp.message_handler(text='Калории')
async def set_gender(message):
    print(f'Сообщение от {message["from"]["first_name"]}')
    UserData.DATA[message["from"]["first_name"]] = {}
    txt = 'Введите свой пол (М/Ж):'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt)
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender)
async def set_age(message, state):
    await state.update_data(gender=message.text)
    txt = 'Введите свой возраст:'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt)
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    txt = 'Введите свой рост:'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt)
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    txt = 'Введите свой вес:'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt)
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    UserData.DATA[message["from"]["first_name"]] |= await state.get_data()
    # locals().update(UserData.DATA[message["from"]["first_name"]])
    print(UserData.DATA)

    data = UserData.DATA[message["from"]["first_name"]]
    try:
        if data['gender'].upper() == 'Ж':
            calories = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) - 161
        elif data['gender'].upper() == 'М':
            calories = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5
        else:
            raise ValueError
    except ValueError:
        txt = 'Вы ввели ошибочные данные'
    else:
        txt = f'Ваша норма калорий по формуле Миффлина-Сан Жеора: {calories}'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt)
    await state.finish()


@dp.message_handler()
async def all_massages(message):
    txt = 'Введите команду /start, чтобы начать общение.'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
