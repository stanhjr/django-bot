import base64
import datetime
import os
import functools

import aiohttp
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
DIGITAL_PROFILE_HOSTNAME = os.getenv('HOSTNAME')
HEADERS = {
    'accept-language': 'en',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}


def add_telegram_id_header(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        telegram_id = kwargs.get('telegram_id')
        if telegram_id:
            HEADERS["telegram-id"] = str(telegram_id)
        return await func(*args, **kwargs)

    return wrapper


def get_list_token():
    string = f'{datetime.datetime.utcnow().strftime("%m-%d")}'.encode()
    return base64.b64encode(string).decode()


@add_telegram_id_header
async def get_categories(telegram_id) -> list:
    async with aiohttp.ClientSession() as session:
        url = f"{DIGITAL_PROFILE_HOSTNAME}/api/categories/"
        async with session.get(url=url, headers=HEADERS) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data


@add_telegram_id_header
async def get_sub_categories(category_id: int, telegram_id) -> dict:
    async with aiohttp.ClientSession() as session:
        url = f"{DIGITAL_PROFILE_HOSTNAME}/api/categories/{category_id}/"
        async with session.get(url=url, headers=HEADERS) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data


@add_telegram_id_header
async def get_products(category_id: int, telegram_id, page: int = None) -> dict:
    async with aiohttp.ClientSession() as session:
        url = f"{DIGITAL_PROFILE_HOSTNAME}/api/categories/{category_id}/list_products/"
        if page:
            url += f"?page={page}"
        async with session.get(url=url, headers=HEADERS) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data
