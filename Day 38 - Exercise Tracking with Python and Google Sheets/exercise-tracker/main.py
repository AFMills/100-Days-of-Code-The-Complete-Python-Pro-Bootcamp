import requests
import os
from datetime import datetime

NUTRITION_API_KEY = os.environ.get("NUTRITION_API_KEY")
NUTRITION_APP_ID = os.environ.get("NUTRITION_APP_ID")

BEARER_TOKEN = os.environ.get("SHEETY_BEARER_TOKEN")

GENDER = os.environ.get("GENDER")
AGE = int(os.environ.get("AGE"))
WEIGHT = int(os.environ.get("WEIGHT"))
HEIGHT = int(os.environ.get("HEIGHT"))

exercise_endpoint = "https://app.100daysofpython.dev/v1/nutrition/natural/exercise"
sheety_endpoint = "https://api.sheety.co/e1ae937fcdabc5fede51c587846bbb21/workoutTracking/workouts"

exercise_query = input("Tell me what exercises you did today: ")

headers = {
    "x-app-id" : NUTRITION_APP_ID,
    "x-app-key" : NUTRITION_API_KEY,
}

bearer_header = {
    "Authorization" : f"Bearer {BEARER_TOKEN}"
}

parameters = {
    "query" : exercise_query,
    "weight_kg" : WEIGHT,
    "height_cm" : HEIGHT,
    "age" : AGE,
    "gender" : GENDER,
}

response = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
result = response.json()
# print(result)


today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheety_inputs = {
        "workout" : {
            "date" : today_date,
            "time" : now_time,
            "exercise" : exercise["name"].title(),
            "duration" : exercise["duration_min"],
            "calories" : exercise["nf_calories"],
        }
    }

sheety_response = requests.post(url=sheety_endpoint, json=sheety_inputs, headers=bearer_header)
print(sheety_response.text)
