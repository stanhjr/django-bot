import os

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ChatType
from aiogram.dispatcher.filters import ChatTypeFilter

from dotenv import load_dotenv, find_dotenv

from api import get_categories, get_sub_categories, get_products, get_stocks, get_shops
from keyboards import (
    get_inline_keyboard_category,
    get_category_name,
    get_start_menu,
    ProductCreator,
    StockCreator,
    get_main_inline_menu, get_shops_inline
)
from messages import MESSAGES

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('BOT_TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def send_stock_photo(stock, callback_query):
    stock_creator = StockCreator(stock)
    caption = await stock_creator.get_caption()
    try:
        file_path = await stock_creator.get_image_path()
        with open(file_path, 'rb') as file:
            await bot.send_photo(callback_query.from_user.id,
                                 caption=caption,
                                 photo=file,
                                 parse_mode="Markdown")
    except Exception as e:
        print(e)


async def send_product_photo(product, callback_query, data):
    product_creator = ProductCreator(product)
    caption = await product_creator.get_caption()
    inline_keyboard = await product_creator.get_inline_keyboard(category_data=data)
    try:
        file_path = await product_creator.get_image_path()
        with open(file_path, 'rb') as file:
            await bot.send_photo(callback_query.from_user.id,
                                 caption=caption,
                                 photo=file,
                                 reply_markup=inline_keyboard,
                                 parse_mode="Markdown")
    except Exception as e:
        print(e)


@dp.message_handler(ChatTypeFilter(chat_type=ChatType.PRIVATE), commands=['start'])
async def start(message: types.Message):
    main_keyboard = await get_start_menu()
    await message.answer(MESSAGES['start'], reply_markup=main_keyboard)


@dp.message_handler(ChatTypeFilter(chat_type=ChatType.PRIVATE), text='🏡 Головне меню')
async def start(message: types.Message):
    # json_data = await get_categories(telegram_id=message.from_user.id)
    inline_keyboard = await get_main_inline_menu()

    # inline_keyboard = await get_inline_keyboard_category(json_data)
    await message.answer("🏡 Головне меню", reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('categories_list'))
async def categories_list(callback_query: types.CallbackQuery):
    json_data = await get_categories(telegram_id=callback_query.from_user.id)

    inline_keyboard = await get_inline_keyboard_category(json_data)
    await bot.send_message(callback_query.from_user.id,
                           text='🏡 Головне меню',
                           reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('cat'))
async def sub_categories(callback_query: types.CallbackQuery):
    category_id = callback_query.data[3:]
    data = await get_sub_categories(category_id, telegram_id=callback_query.from_user.id)
    inline_keyboard = await get_inline_keyboard_category(data)
    category_name = await get_category_name(data)

    await bot.send_message(callback_query.from_user.id,
                           text=category_name,
                           reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda c: c.data == 'stocks')
async def get_stocks_list(callback_query: types.CallbackQuery):
    stocks_list = await get_stocks(telegram_id=callback_query.from_user.id)
    if not stocks_list:
        await bot.send_message(callback_query.from_user.id,
                               text=MESSAGES['not_stocks'])
    else:
        for stock in stocks_list:
            await send_stock_photo(stock=stock, callback_query=callback_query)


@dp.callback_query_handler(lambda c: c.data == 'shops')
async def get_shops_list(callback_query: types.CallbackQuery):
    city_list = await get_shops(telegram_id=callback_query.from_user.id)
    if not city_list:
        await bot.send_message(callback_query.from_user.id,
                               text=MESSAGES['not_shops'])
    else:
        for city in city_list:
            inline_keyboard = await get_shops_inline(shop_list=city['addresses'])
            await bot.send_message(callback_query.from_user.id,
                                   text=city['name'],
                                   reply_markup=inline_keyboard)



@dp.callback_query_handler(lambda c: c.data and c.data.startswith('pro'))
async def get_products_category(callback_query: types.CallbackQuery):
    category_id = callback_query.data[3:]
    data = await get_products(category_id, telegram_id=callback_query.from_user.id)

    for product in data['products']:
        await send_product_photo(product=product, data=data, callback_query=callback_query)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('pag'))
async def get_products_pagination(callback_query: types.CallbackQuery):
    callback_data = callback_query.data[3:]
    category_id, page_num = callback_data.split('_')
    data = await get_products(category_id, page=page_num, telegram_id=callback_query.from_user.id)
    for product in data['products']:
        await send_product_photo(product=product, data=data, callback_query=callback_query)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
