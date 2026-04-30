#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import requests
import os
from flight_search import FlightSearch
from data_manager import DataManager
from flight_data import find_cheapest_flight
from notification_manager import telegram_bot_send_text
import time
from datetime import datetime, timedelta

BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOT_CHATID = os.environ.get("BOT_CHATID")


SHEETY_PRICES_ENDPOINT = os.environ.get("SHEETY_PRICES_ENDPOINT")


def telegram_bot_send_text(bot_message):
    send_text = ("https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage?chat_id="
                 + BOT_CHATID + "&parse_mode=Markdown&text=" + str(bot_message))
    resp = requests.get(send_text)
    return resp.json()



data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()

ORIGIN_CITY_IATA = "LAX"


# Update airport codes in Google Sheets document
for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        time.sleep(2)       # slow down requests to avoid rate limit

print(f"sheet_data:\n{sheet_data}")

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()


# Search for Flights
tomorrow = datetime.now() + timedelta(days=1)
six_months_from_now = datetime.now() + timedelta(days=180)

for destination in sheet_data:
    print(f"Obtaining flights for {destination['city']}...")
    flights = flight_search.check_flights(ORIGIN_CITY_IATA, destination["iataCode"], departure_time=tomorrow,
                                          arrival_time=six_months_from_now)
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: £{cheapest_flight.price}")
    time.sleep(2)

    # Send Message
    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        print(f"Lower price flight to {destination['city']} found!")
        telegram_bot_send_text(bot_message=f"Low price alert! Only £{cheapest_flight.price} to fly from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, on {cheapest_flight.out_date} until {cheapest_flight.return_date}.")
