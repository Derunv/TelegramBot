import requests


def order_status_check(order_number, type: str):
    if type == "ttn":
        try:
            int(order_number)
        except:
            return (
                "Вибачте, але ТТН може складатись лише з цифр. Введіть повторно номер."
            )
        respond = order_get_status_by_ttn(order_number)
    else:
        ...
        # phone_number = format_phone_number(order_number)
        # try:
        #     int(phone_number)
        # except:
        #     return (
        #         "Вибачте, але ТТН може складатись лише з цифр. Введіть повторно номер."
        #     )
        # respond = order_get_status_by_phone(phone_number)
    status = respond["status"]
    if status == "success":
        name = respond["data"]["status"]["name"]
        match name:
            case "Нове замовлення":
                return (
                    "Ваше замовлення прийняте, знаходиться в обробці та готується до\n"
                    " відправки. При потребі ми зв’яжемося для уточнення деталей ❤️"
                )

            case "Потрібен дзвінок":
                return (
                    "Ваше замовлення прийняте, проте перед відправкою нам потрібно\n"
                    " уточнити певну інформацію. Очікуйте дзвінок менеджера найближчим\n"
                    " часом ❤️"
                )

            case "Оплата не пройшла/очікує на оплату":
                return (
                    f"{name}\n"
                    f"Будь ласка, спробуйте ще раз. Сплатити замовлення можна за посиланням:"
                )

            case "Міжнародна відправка":
                return (
                    "Це замовлення з міжнародною доставкою і потребує додаткових уточнень.\n"
                    " Ми зв’яжемося з вами найближчим часом тим методом, який ви обрали при\n"
                    " оформленні замовлення ❤️"
                )

            case "Збирається":
                return (
                    "Ваше замовлення збирається і буде відправлене найближчим часом.\n"
                    " Очікуйте sms з ТТН ❤️"
                )

            case "Зібран":
                return "Ваше замовлення вже зібране і готується до відправки. Очікуйте sms з ТТН ❤️"

            case "Відправлено":
                return "Ваше замовлення в дорозі. Очікуйте сповіщення про прибуття ❤️"

            case "У відділенні/кур’єра":
                return (
                    "Ваше замовлення доставлене і знаходиться у відділенні.\n"
                    " Запрошуємо отримати пакунок ❤️"
                )

            case "Контроль отримання":
                return (
                    "Ваше замовлення доставлене і знаходиться у відділенні. Проте терміни\n"
                    " зберігання обмежені, будь ласка, встигніть отримати свій пакунок ❤️"
                )

            case "Успіх":
                return (
                    "Замовлення було доставлене та отримане. Дякуємо, що обрали ORNER!\n"
                    " Впевнені, наші товари радуватимуть вас довгі роки. До нових зустрічей ❤️"
                )

            case "Провал":
                return (
                    "Шкода, що ви так і не отримали своє замовлення ☹️ Дуже сподіваємось, що\n"
                    "ви повернетеся до нас знову і все ж матимете нагоду насолодитись\n"
                    " нашою продукцією ❤️"
                )

            case _:
                return f"Ми не можемо знайти ваше замовлення {number_of_ttn}. Будь ласка спробуйте ще."
    else:
        return f"Ми не можемо знайти ваше замовлення {number_of_ttn}. Будь ласка спробуйте ще."


def order_get_status_by_ttn(order_number):

    url = f"https://orner.com.ua/api/v1/public/order/{order_number}/status"
    payload = {}
    headers = {
        "Authorization": "Bearer 22122023",
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


def order_get_status_by_phone(phone_number):
    # phone_number = format_phone_number(phone_number)
    # print(phone_number)
    # try:
    #     int(phone_number)
    # except:
    #     return "Вибачте, але ТТН може складатись лише з цифр. Введіть повторно номер."

    url = f"https://orner.com.ua/api/v1/public/order/search?search={phone_number}&page=1&size=10"
    payload = {}
    headers = {
        "Authorization": "Bearer 22122023",
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.text)
    # return response


# print(order_get_status_by_phone("+380963754793"))
