# Домашнее задание по теме "Методы отправки сообщений".
# Цель: написать простейшего телеграм-бота, используя асинхронные функции.
#
# Задача "Он мне ответил!":
# Измените функции start и all_messages так, чтобы вместо вывода в консоль строки
# отправлялись в чате телеграм.
# Запустите ваш Telegram-бот и проверьте его на работоспособность.

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import logging

API = 'XXX'
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(
    filename='tg-bot.log', filemode='w', encoding='utf-8',
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    level=logging.INFO)

@dp.message_handler(commands=['start'])
async def start(message):
    txt = 'Привет! Я бот помогающий твоему здоровью.'
    logging.info(f'Получено сообщение от {message["from"]["first_name"]}: {message["text"]}')
    logging.info(f'Вся информация: {message}')
    await message.answer(txt)
    logging.info(f'Отправлен ответ: {txt}')

@dp.message_handler()
async def all_massages(message):
    txt = 'Введите команду /start, чтобы начать общение.'
    logging.info(f'Получено сообщение от {message["from"]["first_name"]}: {message["text"]}')
    logging.info(f'Вся информация: {message}')
    await message.answer(txt)
    logging.info(f'Отправлен ответ: {txt}')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)