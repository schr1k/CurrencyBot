import aiohttp

from config import config


async def get_currency(currency_from: str, currency_to: str) -> dict:
    url = f'https://rest.coinapi.io/v1/exchangerate/{currency_from}/{currency_to}'
    headers = {'X-CoinAPI-Key': config.API_KEY}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()
