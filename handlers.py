from bot_key import key_telegram as key

from order_status_check_in_crm import order_status_check as order_status

import asyncio

import logging

import sys

from typing import Any, Dict

from aiogram import Bot, Dispatcher, F, Router, html

from aiogram.filters import Command, CommandStart

from aiogram.fsm.context import FSMContext

from aiogram.fsm.state import State, StatesGroup

from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)


TOKEN = key()


form_router = Router()


class Form(StatesGroup):

    start_get_data = State()

    like_bots = State()

    number = State()

    crm_data = State()


# @form_router.message(CommandStart())
# async def command_start(message: Message, state: FSMContext) -> None:
#     print("started command")
#     await state.set_state(Form.name)
#
#     await message.answer(
#         "Hi there! What's your name?",
#         reply_markup=ReplyKeyboardRemove(),
#     )
#     print(message.text)


@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """

    Allow user to cancel any action

    """

    current_state = await state.get_state()

    if current_state is None:

        return

    logging.info("Cancelling state %r", current_state)

    await state.clear()

    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    # print("Form.name, message")

    # await state.update_data(name=message.text)

    await state.set_state(Form.like_bots)

    await message.answer(
        "Привіт! Ласкаво просимо! Я твій чат-бот.\n"
        "Я можу допомогти тобі дізнатися статус замовлення або підписатися на подарунковий бокс.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text="get_order_status",
                    ),
                    KeyboardButton(
                        text="subscribe_to_gift_box",
                    ),
                    KeyboardButton(
                        text="cancel",
                    ),
                ]
            ],
            resize_keyboard=True,
        ),
    )


# @form_router.message(Form.like_bots, F.text.casefold() == "subscribe_to_gift_box")
# async def process_dont_like_write_bots(message: Message, state: FSMContext) -> None:
#
#     data = await state.get_data()
#
#     await state.clear()
#
#     await message.answer(
#         "Not bad not terrible.\nSee you soon.",
#         reply_markup=ReplyKeyboardRemove(),
#     )
#
#     await show_summary(message=message, data=data, positive=False)

# @form_router.message(Form.like_bots, F.text.casefold() == "subscribe_to_gift_box")
# async def process_dont_like_write_bots(message: Message, state: FSMContext) -> None:
#
#     data = await state.get_data()
#
#     await state.clear()
#
#     await message.answer(
#         "Not bad not terrible.\nSee you soon.",
#         reply_markup=ReplyKeyboardRemove(),
#     )
#
#     await show_summary(message=message, data=data, positive=False)


@form_router.message(Form.like_bots, F.text.casefold() == "get_order_status")
async def process_like_write_bots_1(message: Message, state: FSMContext) -> None:

    await state.set_state(Form.start_get_data)
    await message.answer(
        "Виберіть метод отримання данних",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text="TTN",
                    ),
                    KeyboardButton(
                        text="Phone Number",
                        request_contact=True,
                    ),
                    KeyboardButton(
                        text="Cancel",
                    ),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@form_router.message(Form.like_bots)
async def process_unknown_write_bots_2(message: Message) -> None:

    await message.reply("I don't understand you :(")


@form_router.message(Form.start_get_data, F.text.casefold() == "ttn")
async def process_like_write_bots_3(message: Message, state: FSMContext) -> None:

    await state.set_state(Form.crm_data)

    await message.answer(
        "Будь ласка вкажіть номер ТТН",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Form.start_get_data, F.text.casefold() == "phone number")
async def process_like_write_bots_3(message: Message, state: FSMContext) -> None:

    await state.set_state(Form.crm_data)

    await message.answer(
        "Ваш номер ",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Form.crm_data)
async def process_like_write_bots_4(message: Message, state: FSMContext) -> None:
    print(message.text)
    crm_respond = order_status(message.text)
    await message.answer(
        f"{crm_respond}",
        reply_markup=ReplyKeyboardRemove(),
    )


# @form_router.message(Form.number)
# async def process_language(message: Message, state: FSMContext) -> None:
#
#     data = await state.update_data(language=message.text)
#
#     await state.clear()
#
#     if message.text.casefold() == "python":
#
#         await message.reply(
#             "Python, you say? That's the language that makes my circuits light up! 😉"
#         )
#
#     await show_summary(message=message, data=data)
#
#
# async def show_summary(
#     message: Message, data: Dict[str, Any], positive: bool = True
# ) -> None:
#
#     name = data["name"]
#
#     language = data.get("language", "<something unexpected>")
#
#     text = f"I'll keep in mind that, {html.quote(name)}, "
#
#     text += (
#         f"you like to write bots with {html.quote(language)}."
#         if positive
#         else "you don't like to write bots, so sad..."
#     )
#
#     await message.answer(text=text, reply_markup=ReplyKeyboardRemove())


async def main():

    bot = Bot(TOKEN)

    dp = Dispatcher()

    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())
