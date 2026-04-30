import requests
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from pprint import pprint

load_dotenv()       #load environment variables from .env file

SHEETY_PRICES_ENDPOINT = os.environ.get("SHEETY_PRICES_ENDPOINT")

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.user = os.environ["SHEETY_USERNAME"]
        self.password = os.environ["SHEETY_PASSWORD"]
        self.authorization = HTTPBasicAuth(self.user, self.password)
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, auth=self.authorization)
        data = response.json()
        self.destination_data = data["prices"]
        # pprint(data)
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode" : city["iataCode"]
                }
            }
            response = requests.put(url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                                    json=new_data,
                                    auth=self.authorization)
            print(response.text)
