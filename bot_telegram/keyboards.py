from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_inline_keyboard_category(data):
    keyboard = InlineKeyboardMarkup(row_width=1)

    for item in data:
        callback_data = f"cat{item['id']}"
        button = InlineKeyboardButton(item['name'], callback_data=callback_data)
        keyboard.insert(button)

    return keyboard


async def get_inline_subcategories(data):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for item in data:
        callback_data = f"sub{item['id']}"
        button = InlineKeyboardButton(item['name'], callback_data=callback_data)
        keyboard.insert(button)

    return keyboard


async def get_inline_products(data):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for item in data:
        callback_data = f"pro{item['id']}"
        button = InlineKeyboardButton(item['name'], callback_data=callback_data)
        keyboard.insert(button)

    return keyboard
