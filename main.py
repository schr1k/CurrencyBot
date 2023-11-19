import asyncio
import logging
from datetime import datetime

from api import get_currency

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters.command import Command

import config

bot = Bot(token=config.TOKEN)
dp = Dispatcher()

logging.basicConfig(filename="all.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s function: %(funcName)s line: %(lineno)d - %(message)s')
errors = logging.getLogger("errors")
errors.setLevel(logging.ERROR)
fh = logging.FileHandler("errors.log")
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s function: %(funcName)s line: %(lineno)d - %(message)s')
fh.setFormatter(formatter)
errors.addHandler(fh)


# Главная ==============================================================================================================
@dp.message(Command('start'))
async def start(message: Message):
    try:
        await message.answer('Привет, я могу показать актуальный курс обмена практически любой валюты (крипты).\n'
                             'Пример: /usd_rub.\n'
                             'Полный список валют <a href="https://t.me/shr1k_currency_list">здесь</a>.',
                             parse_mode='HTML')
    except Exception as e:
        errors.error(e)


# Обмен ================================================================================================================
@dp.message(F.text.regexp(r'/\w+_\w+'))
async def exchange(message: Message):
    try:
        currency_from, currency_to = [i.upper() for i in message.text[1:].split('_')]
        currency = await get_currency(currency_from, currency_to)
        if 'error' in currency.keys():
            await message.answer('Валюта не найдена.')
        else:
            await message.answer(f'1 {currency_from} = {str(currency["rate"])[:10]} {currency_to}')
    except Exception as e:
        errors.error(e)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    print(f'Бот запущен ({datetime.now().strftime("%H:%M:%S %d.%m.%Y")}).')
    asyncio.run(main())
