import os

from aiogram import types
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup
)


async def get_main_menu():
    home_btn = KeyboardButton("🏡 Головне меню")
    main_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(home_btn)
    return main_menu


async def get_inline_keyboard_category(data):
    keyboard = InlineKeyboardMarkup(row_width=1)
    category_id = None
    is_base = None
    for item in data:
        is_base = isinstance(item.get('sub_categories'), list)
        category_id = item.get('parent_category_for_bot')
        callback_data = f"cat{item['id']}"
        if isinstance(item.get('products'), list) and len(item['products']) > 0:
            callback_data = f"pro{item['id']}"
        button = InlineKeyboardButton(f"{item['name']} ({item['products_count']})", callback_data=callback_data)
        keyboard.insert(button)

    if category_id:
        button = InlineKeyboardButton("⤴ Наверх", callback_data=f'cat{category_id}')
        keyboard.insert(button)
    elif is_base is True:
        button = InlineKeyboardButton("⤴ Наверх", callback_data=f'categories_list')
        keyboard.insert(button)

    return keyboard


async def get_category_name(data):
    for item in data:
        counts_parent_category = '📂' * item['count_parents']
        category_name = f"{counts_parent_category}{item['name']}"
        return category_name


class ProductCreator:

    def __init__(self, product: dict):
        self.product = product

    async def get_caption(self) -> str:
        product_name = f"*{self.product['name'].capitalize()}*"
        code = f"# Код: {self.product['code']}"
        price = f"💰 {self.product['price']}"
        caption = f"{product_name}\n" \
                  f"{code}\n"
        if self.product.get('phone'):
            caption += f"📲 {self.product.get('phone')}\n"
        caption += f"---\n {price}\n ---"
        return caption

    async def get_inline_keyboard(self, category_data: dict) -> types.InlineKeyboardMarkup:
        tg_nickname = self.product.get('tg_nickname')
        inline_keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton('Чат з продавцем', url=f'https://t.me/{tg_nickname}')
        if tg_nickname:
            inline_keyboard.add(button)
        callback_data = f"cat{category_data['parent']}"
        up_button = InlineKeyboardButton("⤴ Наверх", callback_data=callback_data)
        inline_keyboard.add(up_button)
        return inline_keyboard

    async def get_image_path(self) -> str:
        app_directory = os.getcwd()
        return app_directory + self.product['image']
