import requests
import os
from datetime import datetime

PIXELA_ENDPOINT = "https://pixe.la/v1/users"
USERNAME = "theartistformerlyknownasa"
TOKEN = os.environ.get("PIXELA_TOKEN")
GRAPH_ID = "graph1"

user_params = {
    "token" : TOKEN,
    "username" : USERNAME,
    "agreeTermsOfService" : "yes",
    "notMinor" : "yes",
}

# response = requests.post(url=PIXELA_ENDPOINT, json=user_params)       # Create account
# print(response.text)



GRAPH_ENDPOINT = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs"

graph_config = {
    "id" : GRAPH_ID,
    "name" : "Cycling Graph",
    "unit" : "Km",
    "type" : "float",
    "color" : "momiji",
}

headers = {
    "X-USER-TOKEN" : TOKEN
}

# response = requests.post(url=GRAPH_ENDPOINT, json=graph_config, headers=headers)      # Create Graph
# print(response.text)



PIXEL_CREATION_ENDPOINT = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{GRAPH_ID}"
# today = datetime(year=2026, month=2, day=1)
today = datetime.now()

pixel_data = {
    "date" : today.strftime("%Y%m%d"),        #YYYYMMDD
    "quantity" : input("How many kilometers did you cycle today? "),
}

response = requests.post(url=PIXEL_CREATION_ENDPOINT, json=pixel_data, headers=headers)       # Create a pixel
print(response.text)



UPDATE_ENDPOINT = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{GRAPH_ID}/{today.strftime('%Y%m%d')}"

new_pixel_data = {
    "quantity" : "4.5"
}

# response = requests.put(url=UPDATE_ENDPOINT, json=new_pixel_data, headers=headers)      # Update a pixel
# print(response.text)



DELETE_ENDPOINT = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{GRAPH_ID}/{today.strftime('%Y%m%d')}"

# response = requests.delete(url=DELETE_ENDPOINT, headers=headers)        # Delete a pixel
# print(response.text)