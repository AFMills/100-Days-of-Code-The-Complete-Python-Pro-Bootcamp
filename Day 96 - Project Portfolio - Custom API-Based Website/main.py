from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import requests
import os

GOOGLE_KEY = os.environ["API_KEY"]

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Bootstrap(app)

def get_country_info(country):
    restcountries_endpoint = f"https://restcountries.com/v3.1/name/{country}"
    response = requests.get(url=restcountries_endpoint)
    response.raise_for_status()

    country_data = response.json()
    return country_data

def transform_currency_data(country_data):
    currency = []
    currency_complete = (country_data[0]["currencies"])

    for item in currency_complete:
        currency.append(item)
        currency.append(currency_complete[item]["name"])
        currency.append(currency_complete[item]["symbol"])

    return currency

def transform_language_data(country_data):
    languages = []
    languages_complete = country_data[0]["languages"]

    for item in languages_complete:
        language = languages_complete[item]
        languages.append(language)

    return languages

@app.route('/', methods=['GET', 'POST'])
def choose_country():
    if request.method == "GET":
        response = requests.get(url="https://restcountries.com/v3.1/all")
        response.raise_for_status()

        country_data = response.json()
        country_names = []

        for i in range(len(country_data)):
            country = country_data[i]["name"]["common"]
            country_names.append(country)

        countries = sorted(country_names)
        return render_template('index.html', countries=countries)

    if request.method == "POST":
        chosen_country = request.form.get('chosen_country')
        country_data = get_country_info(chosen_country)
        currency = transform_currency_data(country_data)
        languages = transform_language_data(country_data)
        map_link = f"https://www.google.com/maps/embed/v1/place?key={GOOGLE_KEY}&q={country_data[0]['name']['common']}"

        return render_template('country.html', country_data=country_data, currency=currency, languages=languages, map_link=map_link)



if __name__ == "__main__":
    app.run(debug=True)