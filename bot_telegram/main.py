import os

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ChatType
from aiogram.dispatcher.filters import ChatTypeFilter

from dotenv import load_dotenv, find_dotenv

from api import get_categories, get_sub_categories, get_products
from keyboards import get_inline_keyboard_category, get_inline_subcategories, get_category_name, get_up_text, up_inline

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('BOT_TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(ChatTypeFilter(chat_type=ChatType.PRIVATE), commands=['start'])
async def start(message: types.Message):
    json_data = await get_categories()

    inline_keyboard = await get_inline_keyboard_category(json_data)
    await message.answer("Категории:", reply_markup=inline_keyboard)


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
    json_data = await get_sub_categories(category_id)
    inline_keyboard = await get_inline_subcategories(json_data)
    category_name = await get_category_name(json_data)

    await bot.send_message(callback_query.from_user.id,
                           text=f'📂{category_name}',
                           reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('sub'))
async def send_products_details(callback_query: types.CallbackQuery):
    sub_category_id = callback_query.data[3:]
    json_data = await get_products(sub_category_id)

    for product in json_data['products']:
        app_directory = os.getcwd()
        file_path = app_directory + product['image']
        try:
            caption = f"Product Name: {product['name']}\n" \
                      f"Description: {product['description']}\n" \
                      f"Price: {product['price']}"
            with open(file_path, 'rb') as file:
                await bot.send_photo(callback_query.from_user.id, caption=caption, photo=file)
        except Exception as e:
            print(e)
    text = await get_up_text(json_data)
    inline = await up_inline(json_data)
    await bot.send_message(callback_query.from_user.id,
                           text=text,
                           reply_markup=inline)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
