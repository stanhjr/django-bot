from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_inline_keyboard_category(data):
    keyboard = InlineKeyboardMarkup(row_width=1)

    for item in data:
        callback_data = f"cat{item['id']}"
        button = InlineKeyboardButton(f"📂{item['name']}", callback_data=callback_data)
        keyboard.insert(button)

    return keyboard


async def get_inline_subcategories(data):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for item in data:
        callback_data = f"sub{item['id']}"
        button = InlineKeyboardButton(f"📂{item['name']}", callback_data=callback_data)
        keyboard.insert(button)
    button = InlineKeyboardButton("📂 Наверх", callback_data='categories_list')
    keyboard.insert(button)
    return keyboard


async def get_category_name(data):
    for item in data:
        category_name = f"{item['category_name']['name']}"
        return category_name


async def up_inline(data):
    keyboard = InlineKeyboardMarkup(row_width=1)
    callback_data = f"cat{data['category_name']['id']}"
    button = InlineKeyboardButton("📂 Наверх", callback_data=callback_data)
    keyboard.insert(button)
    return keyboard


async def get_up_text(data) -> str:
    category_name = data['category_name']['name']
    sub_category_name = data['name']
    text = f"📂 {category_name}\n" \
           f"📂📂: {sub_category_name}"
    return text
