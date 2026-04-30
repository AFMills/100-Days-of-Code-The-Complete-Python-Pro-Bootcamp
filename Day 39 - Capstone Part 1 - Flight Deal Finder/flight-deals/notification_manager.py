import requests
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOT_CHATID = os.environ.get("BOT_CHATID")

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    pass

def telegram_bot_send_text(bot_message):
    send_text = ("https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage?chat_id="
                 + BOT_CHATID + "&parse_mode=Markdown&text=" + str(bot_message))
    resp = requests.get(send_text)
    return resp.json()