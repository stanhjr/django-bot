import os

from aiogram import types
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup
)


async def get_start_menu():
    home_btn = KeyboardButton("🏡 Головне меню")
    main_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(home_btn)
    return main_menu


async def get_cancel_menu():
    home_btn = KeyboardButton("❌Отмена")
    main_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(home_btn)
    return main_menu


async def get_main_inline_menu():
    keyboard = InlineKeyboardMarkup(row_width=1)

    buttons = [
        InlineKeyboardButton("Товари", callback_data='categories'),
        InlineKeyboardButton("Акції", callback_data='stocks'),
        InlineKeyboardButton("Розпродаж", callback_data='sale_out'),
        InlineKeyboardButton("Наші магазини", callback_data='shops'),
        InlineKeyboardButton("Відгуки та пропозиції", url='https://t.me/feedback_seif_bot'),
        InlineKeyboardButton("Заявка на підбір товару", callback_data='feedback')
    ]

    keyboard.add(*buttons)

    return keyboard


async def get_shops_inline(shop_list: list):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for shop in shop_list:
        keyboard.add(InlineKeyboardButton(f"📍 {shop['address_name']}", url=shop['google_map_link']))
    return keyboard


async def get_inline_keyboard_category(data):
    keyboard = InlineKeyboardMarkup(row_width=1)
    category_id = None
    is_base = None
    for item in data:
        if not item.get('products_count'):
            continue
        is_base = isinstance(item.get('sub_categories'), list)
        category_id = item.get('parent_category_for_bot')
        callback_data = f"cat{item['id']}"
        if isinstance(item.get('products'), list) and len(item['products']) > 0:
            callback_data = f"pro{item['id']}"
        button = InlineKeyboardButton(f"{item['name']} ({item['products_count']})", callback_data=callback_data)
        keyboard.insert(button)

    if category_id:
        button = InlineKeyboardButton("⤴ Назад", callback_data=f'cat{category_id}')
        keyboard.insert(button)
    elif is_base is True:
        button = InlineKeyboardButton("⤴ Назад", callback_data=f'categories_list')
        keyboard.insert(button)

    return keyboard


async def get_category_name(data):
    for item in data:
        counts_parent_category = '📂' * item['count_parents']
        category_name = f"{counts_parent_category}{item['parent_name']}"
        return category_name


class ProductCreator:

    def __init__(self, product: dict):
        self.product = product

    async def get_caption(self) -> str:
        product_name = f"*{self.product['name'].capitalize()}*"
        code = f"# Код: {self.product['code']}"
        price = f"💰 {self.product['price']}"
        description = f"{self.product.get('description')}"
        caption = f"{product_name}\n" \
                  f"{code}\n" \
                  f"{description}\n"

        if self.product.get('phone'):
            caption += f"📲 {self.product.get('phone')}\n"
        caption += f"---\n {price}\n ---"
        return caption

    async def get_inline_keyboard(self, category_data: dict) -> types.InlineKeyboardMarkup:
        tg_nickname = self.product.get('tg_nickname')
        callback_data = f"cat{category_data['parent']}"
        inline_keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton('Чат з продавцем', url=f'https://t.me/{tg_nickname}')
        if tg_nickname:
            inline_keyboard.add(button)

        total_pages = category_data['total_pages']
        next_page = category_data['next_page']
        previous_page = category_data['previous_page']
        if total_pages == 1:
            up_button = InlineKeyboardButton("⤴ Назад", callback_data=callback_data)
            inline_keyboard.add(up_button)
            return inline_keyboard

        pagination_buttons = []
        if previous_page:
            previous_button = InlineKeyboardButton("⬅️", callback_data=f"pag{category_data['id']}_{previous_page}")
            pagination_buttons.append(previous_button)

        pagination_text = InlineKeyboardButton(f"Стр {category_data['current_page']}/{total_pages}", callback_data='3')
        pagination_buttons.append(pagination_text)

        if next_page:
            next_button = InlineKeyboardButton("➡️", callback_data=f"pag{category_data['id']}_{next_page}")
            pagination_buttons.append(next_button)

        inline_keyboard.add(*pagination_buttons)
        up_button = InlineKeyboardButton("⤴ Назад", callback_data=callback_data)
        inline_keyboard.add(up_button)

        return inline_keyboard

    async def get_image_path(self) -> str:
        app_directory = os.getcwd()
        return app_directory + self.product['image']


class StockCreator:

    def __init__(self, stock: dict):
        self.stock = stock

    async def get_image_path(self) -> str:
        return self.stock['image_path']

    async def get_caption(self) -> str:
        return self.stock['text']
