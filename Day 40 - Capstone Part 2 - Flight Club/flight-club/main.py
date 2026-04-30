#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import requests
import os
from flight_search import FlightSearch
from data_manager import DataManager
from flight_data import find_cheapest_flight
from notification_manager import telegram_bot_send_text, send_email
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


customer_data = data_manager.get_customer_emails()
# Verify the name of your email column in your sheet. Yours may be different from mine
customer_email_list = [row["whatIsYourEmailAddress?"] for row in customer_data]
# print(f"Your email list includes {customer_email_list}")


# Search for Flights
tomorrow = datetime.now() + timedelta(days=1)
six_months_from_now = datetime.now() + timedelta(days=180)

for destination in sheet_data:
    # Search for Direct Flights
    print(f"Obtaining direct flights for {destination['city']}...")
    flights = flight_search.check_flights(ORIGIN_CITY_IATA, destination["iataCode"], from_time=tomorrow,
                                          to_time=six_months_from_now)
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: £{cheapest_flight.price}")
    time.sleep(2)

    # Search for Indirect Flights
    if cheapest_flight.price == "N/A":
        print(f"No direct flight to {destination['city']}. Looking for indirect flights...")
        layover_flights = flight_search.check_flights(ORIGIN_CITY_IATA, destination["iataCode"], from_time=tomorrow, to_time=six_months_from_now, is_direct=False)
        cheapest_flight = find_cheapest_flight(layover_flights)
        print(f"Cheapest indirect flight price is: £{cheapest_flight.price}")

    # Send Message
    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        # print(f"Lower price flight to {destination['city']} found!")
        # telegram_bot_send_text(bot_message=f"Low price alert! Only £{cheapest_flight.price} to fly from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, on {cheapest_flight.out_date} until {cheapest_flight.return_date}.")
        if cheapest_flight.stops == 0:
            message = (f"Low price alert! Only £{cheapest_flight.price} to fly direct from "
                       f"{cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, on "
                       f"{cheapest_flight.out_date} until {cheapest_flight.return_date}.")
            telegram_bot_send_text(bot_message=message)
        else:
            message = (f"Low price alert! Only £{cheapest_flight.price} to fly from {cheapest_flight.origin_airport} "
                       f"to {cheapest_flight.destination_airport}, with {cheapest_flight.stops} stop(s) "
                       f"departing on {cheapest_flight.out_date} until {cheapest_flight.return_date}.")
            telegram_bot_send_text(bot_message=message)
        print(f"Check your email. Lower price flight found to {destination['city']}!")

        send_email(email_list=customer_email_list, email_body=message)