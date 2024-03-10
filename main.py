"""
    Використовуйте наступну архітектуру:
        - markups - для кнопок та інших налаштувань
        - handlers - для основної обробки подій та функцій 
        - main - точка входу
    * Окрім архітектури рекомендовано уникати на git ваших токенів, та іншої чутливої інформації 
    
    На git повинні бути наступні додаткові файли:
        - reuqirments.txt - опис ваших залежностей
        - .gitignore - для ігнорування файлів 
        - .flake8 або config.cfg - для налаштування Flake8
        - README - для опису проєкт та його особливостей 
    
    Матеріали для виконання: 
        1. Tutorial: https://www.freecodecamp.org/ukrainian/news/yak-stvoryty-telehram-bota-za-dopomohoyu-python/
        2. Docs Aiogram: https://docs.aiogram.dev/uk-ua/latest/
        3. Create User flow: https://www.mindmeister.com/
        4. Telebot: https://pytba.readthedocs.io/en/latest/quick_start.html
        
    Код в деяких моментах схематичний, підлаштовуйте в залежності від своєї задачу та бібліотеку

"""

# Імпорт бібліотек для роботи із телеграм та мережою
import aiogram

# Потрібно створити файл bot_key.py в якому функція def key_telegram(): повертає token
import asyncio

"""
    Використовуйте наступну архітектуру:
        - markups - для кнопок та інших налаштувань
        - handlers - для основної обробки подій та функцій 
        - main - точка входу
    * Окрім архітектури рекомендовано уникати на git ваших токенів, та іншої чутливої інформації 

    На git повинні бути наступні додаткові файли:
        - reuqirments.txt - опис ваших залежностей
        - .gitignore - для ігнорування файлів 
        - .flake8 або config.cfg - для налаштування Flake8
        - README - для опису проєкт та його особливостей 

    Матеріали для виконання: 
        1. Tutorial: https://www.freecodecamp.org/ukrainian/news/yak-stvoryty-telehram-bota-za-dopomohoyu-python/
        2. Docs Aiogram: https://docs.aiogram.dev/uk-ua/latest/
        3. Create User flow: https://www.mindmeister.com/
        4. Telebot: https://pytba.readthedocs.io/en/latest/quick_start.html

    Код в деяких моментах схематичний, підлаштовуйте в залежності від своєї задачу та бібліотеку

"""

# Імпорт бібліотек для роботи із телеграм та мережою
import aiogram

# Потрібно створити файл bot_key.py в якому функція def key_telegram(): повертає token
import asyncio
from bot_key import key_telegram as key
from aiogram import types, Dispatcher, Bot, Router, F
from aiogram.filters import CommandStart

from aiogram.types import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(
                text="Дізнатися статус замовлення", callback_data="get_order_status"
            )
        ],
        [
            types.KeyboardButton(
                text="Підписатися на подарунковий бокс",
                callback_data="subscribe_to_gift_box",
            )
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, one_time_keyboard=True)
    await message.answer(
        "Привіт! Ласкаво просимо! Я твій чат-бот.\n"
        "Я можу допомогти тобі дізнатися статус замовлення або підписатися на подарунковий бокс.",
        reply_markup=keyboard,
    )


@dp.callback_query(F.data == "get_order_status")
async def get_order_status(callback: types.CallbackQuery):
    # Викликаємо функцію для обробки "Дізнатися статус замовлення"
    await callback.message.answer(
        text="Тут ми повинні реалізувати функціонал для дізнання статусу замовлення."
    )


@dp.callback_query(F.data == "subscribe_to_gift_box")
async def subscribe_to_gift_box(callback: types.CallbackQuery):
    # Викликаємо функцію для обробки "Підписатися на подарунковий бокс"
    await callback.message.answer(
        text="Тут ми повинні реалізувати функціонал для підписки на подарунковий бокс."
    )


async def main() -> None:
    TOKEN = key()
    bot = Bot(TOKEN)

    await dp.start_polling(bot)


# Точка входу в програму
if __name__ == "__main__":
    asyncio.run(main())
