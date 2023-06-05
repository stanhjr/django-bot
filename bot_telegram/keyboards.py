from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup
)


async def is_cancel_category(data) -> bool:
    return False
    if isinstance(data.get('sub_categories'), list) and len(data.get('sub_categories')) == 0:
        if isinstance(data.get('products'), list) and len(data.get('products')) > 1:
            return True
    return False


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


async def up_inline(data):
    keyboard = InlineKeyboardMarkup(row_width=1)
    callback_data = f"cat{data['parent']}"
    button = InlineKeyboardButton("⤴ Наверх", callback_data=callback_data)
    keyboard.insert(button)
    return keyboard


async def get_up_text(data) -> str:
    category_name = data['name']
    sub_category_name = data['name']
    text = f"📂 {category_name}\n" \
           f"📂📂: {sub_category_name}"
    return category_name
