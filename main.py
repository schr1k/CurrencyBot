import logging
import requests

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import config

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(filename="all_log.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
warning_log = logging.getLogger("warning_log")
warning_log.setLevel(logging.WARNING)
fh = logging.FileHandler("warning_log.log")
formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(funcName)s: %(message)s (%(lineno)d)')
fh.setFormatter(formatter)
warning_log.addHandler(fh)


def get_currency(currency_from, currency_to):
    url = f'https://rest.coinapi.io/v1/exchangerate/{currency_from}/{currency_to}'
    headers = {'X-CoinAPI-Key': config.API_KEY}
    response = requests.get(url, headers=headers).json()
    return response


# Главная ==============================================================================================================
@dp.message_handler(commands=['start'])
async def start(message):
    try:
        await message.answer('Привет, я могу показать актуальный курс обмена практически любой валюты (крипты).\n'
                             'Пример: /usdtorub.\n'
                             'Полный список валют <a href="https://t.me/shr1k_currency_list">здесь</a>.',
                             parse_mode='html')
    except Exception as e:
        warning_log.warning(e)


# Обмен ================================================================================================================
@dp.message_handler(regexp=r'\w{1,}to\w{1,}')
async def exchange(message):
    try:
        currency_from, currency_to = [i.upper() for i in message.text[1:].split('to')]
        currency = get_currency(currency_from, currency_to)
        if 'error' in currency.keys():
            await message.answer('Валюта не найдена.')
        else:
            await message.answer(f'1 {currency_from} = {str(currency["rate"])[:10]} {currency_to}')
    except Exception as e:
        warning_log.warning(e)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
