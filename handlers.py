import time
import requests
from telebot import types
from main import API_MONO


def check_status(response: str) -> True:
    match response.status_code:
        case 200:
            print('All okey')
        case 404:
            print(f'Check connection and url {response}')
        case _:
            time.sleep(10)
            print('Something wrong. Try again!')
        
        
def get_exchange_rate(currency_code: int = 980) -> tuple:
    ''' Документація '''
    
    response = requests.get(API_MONO)
    
    if check_status(response):
        response = response.json()
        for item in response:
            if item['currencyCodeA'] == currency_code and item['currencyCodeB'] == 980:  
                return (item['rateBuy'], item['rateSell'])
            
    return None


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Start message")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        amount, currency = message.text.split()
        amount = float(amount)
        currency_code = _

        rate_buy, rate_sell = get_exchange_rate(currency_code)
        if rate_buy and rate_sell:
            converted_amount = amount * rate_buy
            bot.reply_to(message, f"{amount} {currency} = {converted_amount:.2f} UAH")
        else:
            bot.reply_to(message, "Not found")
    except Exception as e:
        bot.reply_to(message, "Something wrong")
