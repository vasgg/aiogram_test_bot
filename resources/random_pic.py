import aiohttp

from config import RANDOM_PIC_URL


async def get_random_pic() -> str:
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        response = await session.get(RANDOM_PIC_URL)
        if response.status == 200:
            return await get_pic_url_from_response(await response.json())
    raise Exception()


async def get_pic_url_from_response(json) -> str:
    return json['url']
