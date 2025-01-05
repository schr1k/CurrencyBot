import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.types import Message

from api import get_currency
from config import config

bot = Bot(token=config.TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


@dp.message(Command('start'))
async def start(message: Message):
    await message.answer('Привет, я могу показать актуальный курс обмена практически любой валюты (крипты).\n'
                         'Пример: /usd_rub.\n'
                         'Полный список валют <a href="https://t.me/shr1k_currency_list">здесь</a>.',
                         parse_mode='HTML')


@dp.message(F.text.regexp(r'/\w+_\w+'))
async def exchange(message: Message):
    currency_from, currency_to = [i.upper() for i in message.text[1:].split('_')]
    currency = await get_currency(currency_from, currency_to)
    if 'error' in currency.keys():
        await message.answer('Валюта не найдена.')
    else:
        await message.answer(f'1 {currency_from} = {str(currency["rate"])[:10]} {currency_to}')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
