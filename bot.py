import json
import time
import requests

import telebot

bot = telebot.TeleBot("<TOKEN>")


def observer():
    """
    Each 5 minutes, I request the famous blockchain.info to give me a fresh price list of it's goodies, then I'll
    send them to all bot members living in the universe.
    """
    while True:
        price_list_raw = json.loads(requests.get("https://blockchain.info/ticker").content)
        price = price_list_raw["USD"]["buy"]
        for item in open("cids.txt", "r").read().split():
            bot.send_message(item, "Current purchase price: $" + str(price))

        time.sleep(5 * 60)


observer()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
    My job is to answer your /start nicely, and store your Chat-ID in a file.
    """
    f = open("cids.txt", "a")
    # in theory, there is a bug  coming from this part. If someone sends /start more than one time,
    # then she's gonna receive more than one message in each loop run. I'm gonna solve this bug when I got some time.
    f.write("\n" + str(message.chat.id))
    f.close()

    bot.reply_to(message,
                 "Mornin' partner, I'm gonna send ya the price list of Crypto-currencies each 5 minutes.")


bot.polling()
