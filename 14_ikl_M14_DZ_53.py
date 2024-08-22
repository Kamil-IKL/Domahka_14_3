import logging
import os
from pprint import pprint

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

from config import *
from keydoards import *
import texts
import database

# делаем базовое логирование
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(
    level=logging.INFO,  # уровень логирования
    filemode='a',  # Название файла # Режим - 'w' для перезаписи, "а" - для добавления
    filename='bot_test.log',  # Название файла
    encoding='utf-8',  # Кодировка
    format='%(asctime)s | %(levelname)s | %(message)s')  # Формат вывода


# запуск своего телеграмбота
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message):
    print('Кто-то вошел в бот')  # это сообщения для меня (вывода на консоль)
    # pprint(message.__dict__)
    # await message.answer(f'Привет, {message.from_user.username} !' + texts.start, reply_markup=kb)
    await message.answer(f'Привет, {message.from_user.first_name} !  ' + texts.start, reply_markup=kb)


@dp.message_handler(text='ИНФОРМАЦИЯ')
async def main_info(message):
    print('Поступил запрос по Информации')  # это сообщения для меня (вывода на консоль)
    await message.answer(texts.info, reply_markup=kb)


@dp.message_handler(text='РАСCЧИТАТЬ НОРМУ КАЛОРИЙ')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=kb_inline)  # активизировал Inline-клаву "Калории"


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    print('Поступил запрос на информацию Formulas')  # это сообщения для меня (вывода на консоль)
    await call.message.answer(texts.formula)
    await call.answer()


# СТАРЫЙ ВАРИАНТ (ДЗ 13_6), весь этот класс закинул в config
# class UserState(StatesGroup):
#     age = State()
#     growth = State()
#     weight = State()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    print('Поступил запрос на расчет Calories')  # это сообщения для меня (вывода на консоль)
    await call.message.answer('Введите свой возраст')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(first=message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(second=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_calories(message, state):
    await state.update_data(third=message.text)
    data = await state.get_data()
    # для мужчин: 10 х вес(кг) + 6,25 x рост(см) – 5 х возраст(г) + 5
    # для женщин: 10 x вес(кг) + 6,25 x рост(см) – 5 x возраст(г) – 161
    await message.answer(f'Ваша норма калорий:\n'
                         f'для мужчин'
                         f'{10 * int(data["first"]) + 6.25 * int(data["second"]) - 5 * int(data["third"]) + 5};\n'
                         f'для женщин'
                         f'{10 * int(data["first"]) + 6.25 * int(data["second"]) - 5 * int(data["third"]) - 161}.')
    await state.finish()


@dp.message_handler(text='КУПИТЬ')
async def get_buying_list(message):
    print('Поступил запрос Купить!!!')  # это сообщения для меня (вывода на консоль)
    for user in database.products:
        username, info, price, image = user[1], user[2], user[3], user[4]
        with open(f'{image}', "rb") as img:
            await message.answer_photo(img, f"Продукт: {username} | Описание: {info} | Цена: {price}", reply_markup=kb)
    await message.answer('Выберите продукт для покупки:',
                         reply_markup=kb_product)  # активизировал Inline-клаву "Продукт"


# ЭТО ВСЕ НЕРАБОЧЕЕ - КАК ОКАЗАЛОСЬ... ВСЕ В МУСОР, НО ОСТАВЛЮ СЕБЕ СМОТРЕТЬ ТЯЖЕЛО РОЖДАЛАСЬ ИСТИНА
# dir_image = 'Image'
# files_image = os.listdir(dir_image)

# ВАРИАНТ 1 - РАБОТАЕТ НЕКОРРЕКТНО
# for user in database.products:
#     username, info, price = user[1], user[2], user[3]
#     for i in files_image:
#         with open(f'Image/{i}', "rb") as img:
#             await message.answer_photo(img, f"Продукт: {username} | Описание: {info} | Цена: {price}",
#                                        reply_markup=kb)
# await message.answer('Выберите продукт для покупки:', reply_markup=kb_product) # активизировал Inline-клаву "Продукт"

# ВАРИАНТ 2 - ТОЖЕ "НЕ ВАРИАНТ" ВЫДАЕТ ОШИБКУ "ValueError: I/O operation on closed file"
# for i in files_image:
#     with open(f'Image/{i}', "rb") as img:
#         for user in database.products:
#             username, info, price = user[1], user[2], user[3]
#             await message.answer_photo(img, f"Продукт: {username} | Описание: {info} | Цена: {price}") #, reply_markup=kb)
# await message.answer('Выберите продукт для покупки:', reply_markup=kb_product)  # активизировал Inline-клаву "Продукт"


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
