import json

import aiohttp

from config import exchange_apikey, EXCHANGE_RATE_URL
from resources.currency_codes import curency_code


class ExchangeResult:

    def __init__(self, amount: float, first_code: str, second_code: str, result_amount: float, conversion_rate: float):
        self.first_code = first_code
        self.amount = amount
        self.second_code = second_code
        self.result_amount = result_amount
        self.conversion_rate = conversion_rate


async def get_exchange_rate_from_message(first_code: str, second_code: str, amount: float) -> ExchangeResult:
    return await get_exchange_response(get_currency_query(first_code, second_code, amount), amount)


def get_currency_code(code: str) -> str:
    if code in curency_code:
        return code
    else:
        raise Exception


def get_currency_query(first_code: str, second_code: str, amount: float) -> str:
    return EXCHANGE_RATE_URL.format(exchange_apikey, first_code, second_code, amount)


async def get_exchange_response(url: str, amount: float) -> json:
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        response = await session.get(url)
        if response.status == 200:
            return get_exchange_rate_from_response(await response.json(), amount=amount)
    raise Exception


def get_exchange_rate_from_response(json, amount) -> ExchangeResult:
    return ExchangeResult(first_code=json['base_code'], amount=amount, second_code=json['target_code'],
                          result_amount=json['conversion_result'], conversion_rate=json['conversion_rate'])
