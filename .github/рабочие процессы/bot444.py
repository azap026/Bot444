import requests
import os
import telegram
from telegram.ext import Updater, CommandHandler

def get_price(crypto):
    url = "https://min-api.cryptocompare.com/data/price?fsym={}&tsyms=USD".format(crypto)
    response = requests.get(url)
    data = response.json()
    return data['USD']

def convert_wallet(update, context):
    try:
        crypto, amount = context.args
        amount = float(amount)
        price = get_price(crypto)
        usd_value = price * amount
        response = "{} {} is worth {:.2f} USD".format(amount, crypto, usd_value)
        context.bot.send_message(chat_id=update.message.chat_id, text=response)
    except (ValueError, KeyError):
        context.bot.send_message(chat_id=update.message.chat_id, text="Invalid command. Use /convert [crypto] [amount]")

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Welcome to the Crypto Converter Bot! Use /convert [crypto] [amount] to convert your wallet.")

token = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telegram.Bot(5994201769:AAEx31L0v6wOrtqx5VRRxHcpmsjMIWvpTeA)
updater = Updater(token=token, use_context=True)

dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('convert', convert_wallet))

updater.start_polling()
