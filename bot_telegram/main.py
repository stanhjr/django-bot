import os

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ChatType
from aiogram.dispatcher.filters import ChatTypeFilter

from dotenv import load_dotenv, find_dotenv

from api import get_categories, get_sub_categories, get_products
from keyboards import (
    get_inline_keyboard_category,
    get_category_name,
    get_main_menu,
    ProductCreator
)

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('BOT_TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(ChatTypeFilter(chat_type=ChatType.PRIVATE), commands=['start'])
async def start(message: types.Message):
    main_keyboard = await get_main_menu()
    await message.answer("Доброго дня", reply_markup=main_keyboard)


@dp.message_handler(ChatTypeFilter(chat_type=ChatType.PRIVATE), text='🏡 Головне меню')
async def start(message: types.Message):
    json_data = await get_categories()

    inline_keyboard = await get_inline_keyboard_category(json_data)
    await message.answer("Головне меню:", reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('categories_list'))
async def categories_list(callback_query: types.CallbackQuery):
    json_data = await get_categories()

    inline_keyboard = await get_inline_keyboard_category(json_data)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Категории',
                           reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('cat'))
async def sub_categories(callback_query: types.CallbackQuery):
    category_id = callback_query.data[3:]
    data = await get_sub_categories(category_id)
    inline_keyboard = await get_inline_keyboard_category(data)
    category_name = await get_category_name(data)

    await bot.send_message(callback_query.from_user.id,
                           text=category_name,
                           reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('pro'))
async def sub_categories(callback_query: types.CallbackQuery):
    category_id = callback_query.data[3:]
    data = await get_products(category_id)
    for product in data['products']:
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


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
