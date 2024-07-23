# Домашнее задание по теме "Инлайн клавиатуры".
# Цель: научится создавать Inline клавиатуры и кнопки на них в Telegram-bot.
#
# Задача "Ещё больше выбора":
# Необходимо дополнить код предыдущей задачи, чтобы при нажатии на кнопку 'Рассчитать'
# присылалась Inline-клавиатруа.
# Создайте клавиатуру InlineKeyboardMarkup с 2 кнопками InlineKeyboardButton:
# 1. С текстом 'Рассчитать норму калорий' и callback_data='calories'
# 2. С текстом 'Формулы расчёта' и callback_data='formulas'
#
# По итогу получится следующий алгоритм:
#
# 1. Вводится команда /start
# 2. На эту команду присылается обычное меню: 'Рассчитать' и 'Информация'.
# 3. В ответ на кнопку 'Рассчитать' присылается Inline меню: 'Рассчитать норму калорий'
# и 'Формулы расчёта'
# 4. По Inline кнопке 'Формулы расчёта' присылается сообщение с формулой.
# 5. По Inline кнопке 'Рассчитать норму калорий' начинает работать машина состояний
# по цепочке.


from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
# import asyncio
import logging

API = 'XXX'
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Информация')
        ]
    ]
)
# kb = ReplyKeyboardMarkup(resize_keyboard=True)
# butt_1 = KeyboardButton(text='Рассчитать')
# butt_2 = KeyboardButton(text='Информация')
# kb.row(butt_1, butt_2)
# kb.insert(butt_1)
# kb.insert(butt_2)

inline_kb = InlineKeyboardMarkup()
inline_butt1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inline_butt2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inline_kb.row(inline_butt1, inline_butt2)

logging.basicConfig(
    filename='tg-bot.log', filemode='a', encoding='utf-8',
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    level=logging.INFO)


def decor_log(func, message: types.Message, txt):
    async def log_writer(*args, **kwargs):
        try:
            logging.info(f'Получено сообщение от {message.from_user.first_name}: {message["text"]}')
        except KeyError:
            logging.info(f'Получено сообщение от {message.from_user.first_name}: Нажата кнопка - {message["data"]}')
        logging.info(f'Вся информация: {message}')
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
async def start(message: types.Message):
    txt = ('Привет! Я бот помогающий твоему здоровью. Хотите узнать сколько калорий '
           'Вам нужно потреблять в день для здорового питания? Нажмите на кнопку "Рассчитать".')
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt, reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message: types.Message):
    print(f'Сообщение от {message.from_user.first_name}')
    txt = 'Выберите опцию:'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt, reply_markup=inline_kb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call: types.CallbackQuery):
    txt = ('Упрощенный вариант формулы Миффлина-Сан Жеора:\n\n'
           'для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5\n'
           'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161\n\n'
           'Формула расчета индекса массы тела (ИМТ):\n\n'
           'ИМТ = вес (кг) / рост (м) ^ 2')
    call.answer = decor_log(call.answer, call, txt)
    await call.message.answer(txt)
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_gender(call: types.CallbackQuery):
    # if not UserData.DATA[call.from_user.first_name]:
    UserData.DATA[call.from_user.first_name] = {}
    txt = 'Введите свой пол (М/Ж):'
    call.answer = decor_log(call.answer, call, txt)
    await call.message.answer(txt)
    await UserState.gender.set()
    await call.answer()


@dp.message_handler(state=UserState.gender)
async def set_age(message: types.Message, state):
    await state.update_data(gender=message.text)
    txt = 'Введите свой возраст:'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt)
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state):
    await state.update_data(age=message.text.replace(',', '.'))
    txt = 'Введите свой рост:'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt)
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state):
    await state.update_data(growth=message.text.replace(',', '.'))
    txt = 'Введите свой вес:'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt)
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state):
    await state.update_data(weight=message.text.replace(',', '.'))
    UserData.DATA[message.from_user.first_name] |= await state.get_data()
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
        imb = round(float(data['weight']) / (float(data['growth']) / 100) ** 2, 1)
    except ValueError or ZeroDivisionError:
        txt = 'Вы ввели ошибочные данные'
    else:
        txt = (f'Ваша норма калорий по формуле Миффлина-Сан Жеора: {calories} калорий\n\n'
               f'Индекс массы тела (ИМТ): {imb} кг/кв.м\n\n'
               f'В соответствии с рекомендациями ВОЗ разработана следующая интерпретация показателей ИМТ:\n\n'
               f'16 и менее — Выраженный дефицит массы тела\n\n'
               f'16 - 18,5 — Недостаточная (дефицит) масса тела\n\n'
               f'18,5 - 25 — Норма\n\n'
               f'25 - 30 — Избыточная масса тела (предожирение)\n\n'
               f'30 - 35 — Ожирение 1 степени\n\n'
               f'35 - 40 — Ожирение 2 степени\n\n'
               f'40 и более — Ожирение 3 степени')
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt)
    await state.finish()


@dp.message_handler(text='Информация')
async def all_massages(message: types.Message):
    txt = 'Я - невероятно крутой бот, который знает секрет как похудеть!'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt)

@dp.message_handler()
async def all_massages(message: types.Message):
    txt = 'Введите команду /start, чтобы начать общение.'
    message.answer = decor_log(message.answer, message, txt)
    await message.answer(txt)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)