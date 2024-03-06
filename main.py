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
from aiogram import types, Dispatcher, Bot, Router
from aiogram.filters import CommandStart

dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(msg: types.Message):
    await msg.answer("Hello World")


async def main() -> None:
    TOKEN = key()
    bot = Bot(TOKEN)

    await dp.start_polling(bot)


# Точка входу в програму
if __name__ == "__main__":
    asyncio.run(main())