import json

import aiohttp.client

from config import weather_apikey, WEATHER_GEO_URL, WEATHER_URL


class Weather:

    def __init__(self, city: str, temp: float, info: str):
        self.city = city
        self.temp = temp
        self.info = info


async def get_weather_from_message(city_name: str) -> Weather:
    return await make_weather_service_query(get_city_weather_url(city_name))

async def get_weather_from_location(latitude: float, longitude: float) -> Weather:
    return await make_weather_service_query(get_city_weather_url_from_location(latitude, longitude))

def get_city_weather_url(city_name: str) -> str:
    return WEATHER_URL.format(city_name, weather_apikey)

def get_city_weather_url_from_location(latitude: float, longitude: float) -> str:
    return WEATHER_GEO_URL.format(latitude, longitude, weather_apikey)

async def make_weather_service_query(url: str) -> json:
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        if response.status == 200:
            return get_weather_from_response(await response.json())
    raise Exception


def get_weather_from_response(json) -> Weather:
    return Weather(json['name'], json['main']['temp'], json['weather'][0]['description'])
