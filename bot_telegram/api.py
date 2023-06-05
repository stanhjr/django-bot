import base64
import datetime
import os

import aiohttp
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
DIGITAL_PROFILE_HOSTNAME = os.getenv('HOSTNAME')
HEADERS = {
    'accept-language': 'en',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}


def get_list_token():
    string = f'{datetime.datetime.utcnow().strftime("%m-%d")}'.encode()
    return base64.b64encode(string).decode()


async def get_categories() -> list:
    async with aiohttp.ClientSession() as session:
        url = f"{DIGITAL_PROFILE_HOSTNAME}/api/categories/"
        async with session.get(url=url, headers=HEADERS) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data


async def get_sub_categories(category_id: int) -> dict:
    async with aiohttp.ClientSession() as session:
        url = f"{DIGITAL_PROFILE_HOSTNAME}/api/categories/{category_id}/"
        async with session.get(url=url, headers=HEADERS) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data


async def get_products(category_id: int) -> dict:
    async with aiohttp.ClientSession() as session:
        url = f"{DIGITAL_PROFILE_HOSTNAME}/api/categories/{category_id}/list_products/"
        async with session.get(url=url, headers=HEADERS) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data
