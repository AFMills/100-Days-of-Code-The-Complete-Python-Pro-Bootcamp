import requests
import os
# from twilio.rest import Client

OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
# In the Terminal, we can store the API key securely using the following command: setx KEY "VALUE" (requires a restart to access)
API_KEY = os.environ.get("OWM_API_KEY")

BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOT_CHATID = os.environ.get("BOT_CHATID")

def telegram_bot_send_text(bot_message):
    send_text = ("https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage?chat_id="
                 + BOT_CHATID + "&parse_mode=Markdown&text=" + str(bot_message))
    resp = requests.get(send_text)
    return resp.json()



weather_params = {
    "lat" : 33.448376,
    "lon" : -112.074036,
    "appid" : API_KEY,
    "cnt" : 4,
}

response = requests.get(url=OWM_ENDPOINT, params=weather_params)
response.raise_for_status()
weather_data = response.json()
# print(weather_data["list"][0]["weather"][0]["id"])

will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    telegram_bot_send_text("Bring an umbrella")