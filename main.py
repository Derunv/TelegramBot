
    await message.answer(
        "І своє прізвище: ",
        reply_markup=ReplyKeyboardRemove(),
    )
    print(message.text)


@form_router.message(Form.user_last_name_for_subscribe)
async def user_last_name(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.user_phone_number_for_subscribe)

    await message.answer(
        "Тепер, будь ласка, вкажіть свій номер телефону: ",
        reply_markup=ReplyKeyboardRemove(),
    )
    print(message.text)


@form_router.message(Form.user_phone_number_for_subscribe)
async def user_last_name(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.user_addresses_for_subscribe)

    await message.answer(
        "Щоб ми могли доставити бокс Новою поштою, нам потрібна ваша адреса. "
        "Будь ласка, вкажіть населений пункт 👇🏻: ",
        reply_markup=ReplyKeyboardRemove(),
    )
    print(message.text)


@form_router.message(Form.user_addresses_for_subscribe)
async def user_last_name(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.user_branch_number_for_subscribe)

    await message.answer(
        "І Номер відділення: ",
        reply_markup=ReplyKeyboardRemove(),
    )
    print(message.text)


@form_router.message(Form.user_branch_number_for_subscribe)
async def pay(message: Message, state: FSMContext) -> None:
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


@form_router.message(Form.pay_for_subscribe, F.text.casefold() == "оплата liqpay")
async def process_like_write_bots_4(message: Message, state: FSMContext) -> None:
    is_subscribe = subscribe()

    await message.answer(
        f"{is_subscribe}",
        reply_markup=ReplyKeyboardRemove(),
    )
    print(message.text)


# ====================================================================================================== YOUR FUNCTIONS


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
    crm_respond = order_status()
    await message.answer(
        f"{crm_respond}",
        reply_markup=ReplyKeyboardRemove(),
    )


# =========================================================================================================== MAIN


async def main():
    TOKEN_API = key()
    bot = Bot(TOKEN_API)
    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())
