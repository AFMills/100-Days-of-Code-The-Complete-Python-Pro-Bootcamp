import requests
from datetime import datetime
#
# response = requests.get(url="http://api.open-notify.org/iss-now.json")
# response.raise_for_status()         # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
#
# longitude = response.json()["iss_position"]["longitude"]
# latitude = response.json()["iss_position"]["latitude"]
#
# iss_position = (longitude, latitude)
# print(iss_position)
#
#
# # Response Codes:
# #   1XX: Hold on
# #   2XX: Here you go
# #   3XX: Go away (you don't have permission)
# #   4XX: You screwed up
# #   5XX: The server screwed up

MY_LAT = 51.507351
MY_LNG = -0.127758

parameters = {
    "lat" : MY_LAT,
    "lng" : MY_LNG,
    "formatted" : 0
}
response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = data["results"]["sunrise"].split("T")[1].split(":")[0]
sunset = data["results"]["sunset"].split("T")[1].split(":")[0]

print(sunrise)
print(sunset)

time_now = datetime.now()
print(time_now.hour)

