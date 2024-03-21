import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    Message,
)

from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# from bot_key import TOKEN_API
from config.bot_key import (
    key_telegram as key,
)  # This function returns the bot token "some string"
from utils.order_status_check_in_crm import order_status_check as order_status
from utils.append_data_to_google_sheet import append_data_to_sheet as append_data

# =========================================================================================================== FUNCTIONS

TOKEN_API = key()
form_router = Router()
user_data: list = []  # Data that will be added to Google Sheet


class Form(StatesGroup):
    start_get_data = State()  # User choose to Get order status or to subscribe

    # Order status flow
    user_chooses_a_method = State()
    number = State()
    crm_data = State()

    # Subscribe flow
    user_phone_number_for_subscribe = State()
    user_first_name_for_subscribe = State()
    user_last_name_for_subscribe = State()
    user_addresses_for_subscribe = State()
    user_branch_number_for_subscribe = State()
    pay_for_subscribe = State()
    user_data_for_subscribe = State()


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

    await state.set_state(Form.user_chooses_a_method)

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


@form_router.message(
    Form.user_chooses_a_method, F.text.casefold() == "get_order_status"
)
async def user_chooses_a_method(message: Message, state: FSMContext) -> None:

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


# ======================================================================================================== MY FUNCTIONS


@form_router.message(
    Form.user_chooses_a_method, F.text.casefold() == "subscribe_to_gift_box"
)
async def user_first_name(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.user_first_name_for_subscribe)

    await message.answer(
        "Для того, щоб оформити підписку на бокс, вкажіть, будь ласка, своє ім'я: ",
        reply_markup=ReplyKeyboardRemove(),
    )
    user_data.append(message.text)


@form_router.message(Form.user_first_name_for_subscribe)
async def user_last_name(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.user_last_name_for_subscribe)
    await message.answer(
        "І своє прізвище: ",
        reply_markup=ReplyKeyboardRemove(),
    )
    user_data.append(message.text)


@form_router.message(Form.user_last_name_for_subscribe)
async def user_last_name(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.user_phone_number_for_subscribe)

    await message.answer(
        "Тепер, будь ласка, вкажіть свій номер телефону: ",
        reply_markup=ReplyKeyboardRemove(),
    )
    user_data.append(message.text)


@form_router.message(Form.user_phone_number_for_subscribe)
async def user_last_name(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.user_addresses_for_subscribe)

    await message.answer(
        "Щоб ми могли доставити бокс Новою поштою, нам потрібна ваша адреса. "
        "Будь ласка, вкажіть населений пункт 👇🏻: ",
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.append(message.text)


@form_router.message(Form.user_addresses_for_subscribe)
async def user_last_name(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.user_branch_number_for_subscribe)

    await message.answer(
        "І Номер відділення: ",
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.append(message.text)


@form_router.message(Form.user_branch_number_for_subscribe)
async def pay(message: Message, state: FSMContext) -> None:
    user_data.append(message.text)

    await state.set_state(Form.pay_for_subscribe)

    await message.answer(
        "Вже майже все 🙃 \n"
        "Для завершення оформлення підписки здійсніть, будь ласка, свою першу оплату: ",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text="Оплата liqpay", url="https://www.liqpay.ua/authorization"
                    ),
                ]
            ],
            resize_keyboard=True,
        ),
        # reply_markup=ReplyKeyboardRemove(),
    )


def subscribe():
    return (
        "Дякуємо, підписка на подарунковий бокс від ORNER успішно активована! 🎉\n"
        "	Очікуйте повідомлення з номером накладної"
    )


@form_router.message(Form.pay_for_subscribe, F.text.casefold() == "оплата liqpay")
async def post_payment_processed(message: Message, state: FSMContext) -> None:
    is_subscribe = subscribe()

    await message.answer(
        f"{is_subscribe}",
        reply_markup=ReplyKeyboardRemove(),
    )

    append_data([user_data])


# ====================================================================================================== YOUR FUNCTIONS


@form_router.message(Form.user_chooses_a_method)
async def process_unknown_write_bots_2(message: Message) -> None:
    await message.reply("I don't understand you :(")


@form_router.message(Form.start_get_data, F.text.casefold() == "ttn")
async def get_status_using_ttn(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.crm_data)

    await message.answer(
        "Будь ласка вкажіть номер ТТН",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Form.start_get_data)
async def get_status_using_phone_number(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.crm_data)

    crm_respond = order_status(message.contact.phone_number, "phone")

    await message.answer(
        f"Ваш номер {message.contact.phone_number}\n" f"{crm_respond}",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Form.crm_data)
async def send_request_to_server(message: Message, state: FSMContext) -> None:
    crm_respond = order_status(message.text, "ttn")

    await message.answer(
        f"{crm_respond}",
        reply_markup=ReplyKeyboardRemove(),
    )


# =========================================================================================================== MAIN


async def main():
    bot = Bot(TOKEN_API)
    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())
