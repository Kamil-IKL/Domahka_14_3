from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# обычная клава с обычными кнопками

# СТАРЫЙ ВАРИАНТ (ДЗ 13_6)
# kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
# button_1 = KeyboardButton(text='Рассчитать норму калорий')
# button_2 = KeyboardButton(text='Информация')
# kb.row(button_1, button_2) # запуск кнопок в линию

# Клава "Старт"
kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='ИНФОРМАЦИЯ'),
            KeyboardButton(text='РАСCЧИТАТЬ НОРМУ КАЛОРИЙ'),
            KeyboardButton(text='КУПИТЬ')
        ]
    ], resize_keyboard=True
)

# Inline-клавиатура с Inline-кнопками

# СТАРЫЙ ВАРИАНТ (ДЗ 13_6)
# kb_inline = InlineKeyboardMarkup()
# button_1_inline = InlineKeyboardButton(text='Расчет нормы', callback_data='calories')
# button_2_inline = InlineKeyboardButton(text='Формула расчета', callback_data='formulas')
# kb_inline.add(button_1_inline, button_2_inline)

# Inline-клава "Калории"
kb_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Расчет нормы', callback_data='calories'),
            InlineKeyboardButton(text='Формула расчета', callback_data='formulas')
        ]
    ], resize_keyboard=True
)

# Inline-клаву "Продукт"
kb_product = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Продукт1', callback_data='product_buying'),
            InlineKeyboardButton(text='Продукт2', callback_data='product_buying'),
            InlineKeyboardButton(text='Продукт3', callback_data='product_buying'),
            InlineKeyboardButton(text='Продукт4', callback_data='product_buying')
        ]
    ], resize_keyboard=True
)