# Домашнее задание по теме "Хендлеры обработки сообщений".
# Цель: написать простейшего телеграм-бота, используя асинхронные функции.
#
# Подготовка:
# Выполните все действия представленные в этих видео, создав и подготовив Telegram-бот
# для дальнейших заданий:
# Инструкция по созданию телеграм бота.
# Set Up конфигурации бота для библиотеки aiogram.
#
# Задача "Бот поддержки (Начало)":
# К коду из подготовительного видео напишите две асинхронные функции:
# 1. start(message) - печатает строку в консоли 'Привет! Я бот помогающий твоему здоровью.'.
# Запускается только когда написана команда '/start' в чате с ботом. (используйте
# соответствующий декоратор)
# 2. all_massages(message) - печатает строку в консоли 'Введите команду /start, чтобы
# начать общение.'. Запускается при любом обращении не описанном ранее. (используйте
# соответствующий декоратор)
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
    print(txt)
    logging.info(f'Получено сообщение от {message["from"]["first_name"]}: {message["text"]}')
    logging.info(f'Вся информация: {message}')
    logging.info(f'Отправлен ответ: {txt}')

@dp.message_handler()
async def all_massages(message):
    txt = 'Введите команду /start, чтобы начать общение.'
    print(txt)
    logging.info(f'Получено сообщение от {message["from"]["first_name"]}: {message["text"]}')
    logging.info(f'Вся информация: {message}')
    logging.info(f'Отправлен ответ: {txt}')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)